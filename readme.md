# seequality powerbi python toolkit
This toolkit is made by seequality.net and is build to help developers working with PowerBI.

## prerequisites
1) Python (3.6.4)
2) ChromeDriver (2.41)
3) Require python packages
    - dataclasses (0.6)
    - selenium (3.12.0)
    - beautifulsoup4 (4.6.3)

## config
Before start please adjust the config file and change the name from "config_sample.json" to "config.json"

## sample usage
Script takes two arguments:
1) m - method name
2) o - output name

get-and-check-all - get all elements from powerbi.com and check errors in workspaces dashboards and workspaces reports
```
python seequality_powerbi_python_toolkit.py -m "get-and-check-all" -o "file"
```
get-and-check-all - get workspaces and dashboards elements from powerbi.com and check errors in workspace dashboards
```
python seequality_powerbi_python_toolkit.py -m "get-and-check-dashboards-only" -o "file"
```

Avaliable method options are:
* get-and-check-all
* get-and-check-dashboards-only


Avaliable output options are:
* file
* console

## sample output
The output of the script is the text file with all of the Power BI element's names and url's including the information about the elements that contains at least one visual error. Apart from the text file there will be also the screenshoot with the visual error if any. 
```
app > <app_name> > <app_url>
workspace > <workspace_name> > <workspace_url>
workspace report > <workspace_name> > <workspace_report_name> > <workspace_report_url>
workspace dashboard > <workspace_name> > <dashboard_name> > <workspace_dashboard_url>
workspace report tabs >  > <workspace_name> > <workspace_report_name> > <workspace_report_url> > <workspace_report_tab_name> > <workspace_report_tab_url>
workspace report tabs visual error >  > <workspace_name> > <workspace_report_name> > <workspace_report_url> > <workspace_report_tab_name> > <workspace_report_tab_url>
workspace dashboard visual error > <workspace_name> > <dashboard_name> > <workspace_dashboard_url>
```
Sample screenshot:

![Visual error screnshot](https://pl.seequality.net/wp-content/uploads/2018/08/visualerror_20180819_112554_2f4acbd67d90495eb14a6fad44ca223a.png)

## versions
0.9 - current version

## known issues
1) if there is no dashboards in the workspace script will not be able to get the list of the reports. If there is no dashbaords the link is redirecting to the list of dashboards even if the link is set to the reports. The workaround would be to always create at least one dashboard. The dashboards can be set as "not to publish" for the app which should be fine.
2) if there are multiple tabs with the same name in one report those tabs will not be checked. The workaround would be to change the names and avoid duplicates. Please note that if there is any duplciate they will be saved in the output data directory
3) print screen of workspace dashboard might be not accurate. There is a problem with taking a fullscreen print screen for chromium web driver. There needs to be custom method implemented or firefox web driver used to solve the issue. This will be taken into consideration for the next release. Please note that for the reports tab's errors in most cases the screnshot should be just fine 

## future improvements
1) add getting the particular error message for each visual's error
2) add checking only single workspace/app/report
3) add checking visual errors for reports/dashboards imported from the flat file
4) get rid of hardcoded sensitive data in the config file
4) performance improvements - currently it's taking around 60 mintues to get and check about 15 apps, 20 workspaces, 50 reports, 20 dashboards, 100 tabs

### More info
1) Polish blog post: https://pl.seequality.net/power-bi-wykrywanie-bledow-na-opublikowanych-raportach
2) English blog post: not avaliable yet