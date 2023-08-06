#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" eMASS integration to the CLI to allow support for eMASS documents """

# standard python imports
import os
from pathlib import Path

import click
import pandas as pd
from openpyxl import load_workbook

from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.utils.app_utils import (
    error_and_exit,
    get_current_datetime,
    get_file_type,
    reformat_str_date,
)
from models.app_models.click import regscale_id

logger = create_logger()
SKIP_ROWS: int = 7


@click.group()
def emass():
    """[BETA] Performs bulk processing of eMASS files (Upload trusted data only)."""


@emass.command("populate_controls")
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the eMASS controls document.",
    help="Enter the full file path of the eMASS controls document to populate with RegScale data.",
)
@regscale_id(help="Enter the desired SSP ID # from RegScale.")
def populate_controls(file_name: click.Path, regscale_id: int) -> None:
    """
    [BETA] Populate controls from a System Security Plan in RegScale into an eMASS formatted excel workbook.
    """
    # make sure the user gave a path to an Excel workbook
    if get_file_type(file_name) not in [".xlsx", ".xls"]:
        error_and_exit(
            "Please provide a file path to an Excel workbook in .xlsx or .xls format."
        )

    # convert file_name to a Path object
    file_name = Path(file_name)

    # initialize the Application and API classes
    app = Application()
    api = Api(app)

    # update the timeout for the API
    api.timeout = 30

    # create the GraphQL query
    query = (
        """
    query {
      controls:controlImplementations(
        take: 50
        skip: 0
        where: {
          parentId: { eq: """
        + str(regscale_id)
        + """ }
          parentModule: { eq: "securityplans" }
          assessments: { any: true }
        }
      ) {
        items {
          id
          control {
            controlId
          }
          assessments {
            actualFinish
            status
            summaryOfResults
            leadAssessor {
              firstName
              lastName
            }
          }
        }
        totalCount
        pageInfo {
          hasNextPage
        }
      }
    }
    """
    )

    # get the data from GraphQL
    response = api.graph(query=query)

    controls = response["controls"]["items"]

    if len(controls) > 0:
        logger.info(
            "Received %s/%s controls with Assessments from SSP # %s.",
            len(controls),
            response["controls"]["totalCount"],
            regscale_id,
        )
    else:
        error_and_exit(
            "The RegScale SSP provided no data. Please verify the ID and try again."
        )

    # load the Excel file in pandas to find row # to update the data
    file_data = pd.read_excel(file_name, skiprows=5)

    # load the workbook using openpyxl to retain worksheet styling
    wb = load_workbook(file_name)

    # set the sheet to the first sheet in the provided workbook
    sheet = wb.active

    # convert to a dictionary
    file_data_dict = file_data.to_dict()

    # convert the control names to match RegScale control names
    try:
        raw_controls = [v.lower() for v in file_data_dict["Control Acronym"].values()]
        formatted_controls = [
            v.lower().replace("(", ".").replace(")", "")
            for v in file_data_dict["AP Acronym"].values()
        ]
    except KeyError:
        error_and_exit(f"{file_name.name} doesn't match the expected eMASS format.")

    # create variable to count number of rows updated
    update_counter: int = 0

    # iterate through the controls to map them to the provided Excel workbook
    for control in controls:
        found_flag: bool = False

        # figure out the row for the control mapping
        if control["control"]["controlId"].lower() in raw_controls:
            row_number = raw_controls.index(control["control"]["controlId"].lower())
            found_flag = True
        elif control["control"]["controlId"].lower() in formatted_controls:
            row_number = formatted_controls.index(
                control["control"]["controlId"].lower()
            )
            found_flag = True

        if not found_flag:
            logger.error(
                "Unable to locate RegScale control # %s - %s to %s.",
                control["control"]["controlId"],
                control["id"],
                file_name.name,
            )
            # skip to the next control
            continue

        # get the assessment for the control
        assessment = control["assessments"][0]

        # determine compliance status
        if assessment["status"] == "Pass":
            compliance_status = "Compliant"
        elif assessment["status"] in ["Fail", "Partial Pass"]:
            compliance_status = "Non-Compliant"
        else:
            compliance_status = "Not Applicable"

        # reformat the assessment actualFinish date if it is populate
        finish_date = (
            reformat_str_date(assessment["actualFinish"])
            if assessment["actualFinish"]
            else ""
        )

        # map the control to the Excel spreadsheet, add SKIP_ROWS constant to the row number
        # because openpyxl doesn't use 0 indexing, and we have to skip the table headers
        sheet[f"L{row_number + SKIP_ROWS}"] = compliance_status
        sheet[f"M{row_number + SKIP_ROWS}"] = finish_date
        sheet[
            f"N{row_number + SKIP_ROWS}"
        ] = f'{assessment["leadAssessor"]["firstName"]} {assessment["leadAssessor"]["lastName"]}'
        sheet[f"O{row_number + SKIP_ROWS}"] = assessment["summaryOfResults"]

        # update the counter
        update_counter += 1

    # add the date and time to the output filename
    output_name = Path(
        os.path.join(
            file_name.parent,
            file_name.stem
            + get_current_datetime("_Updated_%Y%m%d_%H%M%S")
            + file_name.suffix,
        )
    )

    # save the updated workbook
    wb.save(output_name)
    logger.info(
        "%s has been updated with %s entries.", output_name.name, update_counter
    )
