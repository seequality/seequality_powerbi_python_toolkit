from powerbi_toolkit.toolkit import Toolkit
import collections
import argparse


# handling arguments
parser = argparse.ArgumentParser(description='seequality powerbi toolkit v 0.9')
parser.add_argument('-m','--method', help='Method to invoke. Default: get-and-check-all', required=False, default="get-and-check-all")
parser.add_argument('-o','--output', help='Output method. Default: file', required=False, default="file")
args = vars(parser.parse_args())
is_argument_list_correct = False


# check arguments values
if (args["method"] in ["get-and-check-all", "get-and-check-dashboards-only"]) and (args["output"] in ["file", "console"]):
    is_argument_list_correct = True


if is_argument_list_correct:
    
    # initialize 
    toolkit = Toolkit(arguments = args)

    if args["method"] == 'get-and-check-all':
        toolkit.login()
        toolkit.getApps()
        toolkit.getWorkspaces()
        toolkit.getWorkspacesDashboards()
        toolkit.checkWorkspaceDashboardVisualsErrors()
        toolkit.getWorkspacesReports() 
        toolkit.getWorkspacesReportsTabs()
        toolkit.checkReportTabsVisualsErrors()
        toolkit.dispose()

    elif args["method"] == 'get-and-check-dashboards-only':
        toolkit.login()
        toolkit.getWorkspaces()
        toolkit.getWorkspacesDashboards()
        toolkit.checkWorkspaceDashboardVisualsErrors()
        toolkit.dispose()


    if args["output"] == 'file':
        toolkit.saveData()
    elif args["output"] == 'console':
        toolkit.printData()
        
else:
    print ("incorrect argument value")
