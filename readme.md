### seequality powerbi python toolkit
This toolkit is made by seequality.net members and is build to help when working with PowerBI.

# config
Before start please adjust the config file and change the name from "config_sample.json" to "config.json"

# sample usage
python seequality_powerbi_python_toolkit.py -m "get-and-check-all" -o "file"
python seequality_powerbi_python_toolkit.py -m "get-and-check-dashboards-only" -o "file"

# versions
0.9 - current version

# known issues
1) if there is no dashboards in the workspace script will not be able to get the list of the reports. There is an issue and if there is no dashbaords the link is redirecting to the list of dashboards even if the link is set to the reports. The workaround would be to always create at least one dashboard. The dashboards can be set as "not to publish" for the app which should be fine.
2) if there are multiple tabs with the same name in one report those tabs will not be checked. The workaround would be to change the names and avoid duplicates. Please note that id there is any duplciate they will be saved in the output data directory
3) print screen of workspace dashboard might be not accurate. There is a problem with taking a fullscreen print screen for chromium web driver. There needs to be custom method implemented or firefox web driver used to solve the issue. This will be taken into consideration for the next release. Please note that for the reports tab's errors in most cases it should be fine 

# future improvements plan
1) add getting the particular error message for each visual's error
2) add checking only single workspace/app/report
3) add checking visual errors for reports/dashboards imported from the flat files
4) get rid of hardcoded sensitive data in the config file
4) performancec improvements