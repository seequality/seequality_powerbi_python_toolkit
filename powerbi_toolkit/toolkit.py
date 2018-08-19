# internal
from powerbi_toolkit.classes import PowerbiApp
from powerbi_toolkit.classes import PowerbiWorkspace
from powerbi_toolkit.classes import PowerbiWorkspaceDashboard
from powerbi_toolkit.classes import PowerbiWorkspaceReport
from powerbi_toolkit.classes import PowerbiWorkspaceReportTab
from powerbi_toolkit.classes import ScreenshotType


# external
import os  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import os
import time
import urllib.request
import datetime
import uuid
import collections
import logging
import json



class Toolkit:


    def __init__(self, arguments: dict):
 
        self.CONFIG_FILE_PATH = os.path.abspath(__file__ + "/../../config/config.json")

        with open(self.CONFIG_FILE_PATH) as f:
            config_data = json.load(f)

        self.base_Url = config_data["tech"]["base_url"]
        self.base_url_after_login = config_data["tech"]["base_url_after_login"]
        self.chromium_path = config_data["tech"]["chromium_path"]
        self.time_sleep_normal_seconds = config_data["tech"]["time_sleep_normal_seconds"]
        self.time_sleep_report_seconds = config_data["tech"]["time_sleep_report_seconds"]
        self.page_load_timeout = config_data["tech"]["page_load_timeout"]
        self.powerbi_user_email = config_data["user"]["powerbi_user_email"]
        self.powerbi_user_name = config_data["user"]["powerbi_user_name"]
        self.powerbi_user_password = config_data["user"]["powerbi_user_password"]
        self.log_img_directory_path = config_data["system"]["log_img_directory_path"]
        self.log_save_code_error_screenshot = config_data["system"]["log_save_code_error_screenshot"]
        self.log_app_directory_path = config_data["system"]["log_app_directory_path"]
        self.log_data_directory_path = config_data["system"]["log_data_directory_path"]

        # structures
        self.app_list = []
        self.workspae_list = []
        self.workspace_report_list = []
        self.workspace_dashboard_list = []
        self.workspace_report_tab_list = []
        self.workspace_report_tab_duplicates_list = []
        self.workspace_report_tab_visual_errors_list = []
        self.workspace_dashboard_visual_errors_list = []

        # initialize
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--log-level=2")
        #self.browser = webdriver.Chrome(executable_path=self.chromium_path) # to run without headless mode
        self.browser = webdriver.Chrome(executable_path=self.chromium_path, chrome_options=chrome_options)
        self.browser.execute_script("document.body.style.zoom='100'")
        self.is_logged_in = False
        self.current_run_guid = uuid.uuid4().hex


        #logging
        logging.basicConfig(level=logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler(self.log_app_directory_path + "applog.txt")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        # for debugging
        #console_handler = logging.StreamHandler()
        #console_handler.setLevel(logging.INFO)
        #console_handler.setFormatter(formatter)
        #self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.propagate = False

        # log start and log used arguments
        self.logger.info("Starting toolkit with the following parameters. Method: <" + arguments["method"] + ">, output: <" + arguments["output"] + ">")





    def dispose(self):

        self.browser.quit()





    def log(self, log_message: str):
        
        print ("Log message: " + log_message)

        full_log_message = datetime.datetime.today().strftime("%Y%m%d_%H%M%S") + " > guid: " + self.current_run_guid + " > message: " + log_message
        
        current_output_file_name =  self.log_app_directory_path + "log_" + ".txt"
        
        with open(current_output_file_name, 'a') as output_file:
        
            output_file.write(full_log_message + "\n")  




    def saveScreenshot(self, screenshotType: ScreenshotType):
        
        if ((screenshotType.name == ScreenshotType.CodeError and self.log_save_code_error_screenshot == True) or screenshotType.name != ScreenshotType.CodeError):
            current_file_name =  self.log_img_directory_path + screenshotType.value + datetime.datetime.today().strftime("_%Y%m%d_%H%M%S_") + self.current_run_guid + ".png"

            self.browser.get_screenshot_as_file(current_file_name)
            
            return current_file_name
        else:
            return "none"
    



    def printData(self):
       
        for app in self.app_list:
            print ("app > " + app.AppName + " > " + app.AppUrl)

        for workspace in self.workspae_list:
            print ("workspace > " + workspace.WorkspaceName + " > " + workspace.WorkspaceUrl)

        for workspace_report in self.workspace_report_list:
            print ("workspace report > " + workspace_report.WorkspaceName + " > " + workspace_report.WorkspaceReportName + " > " + workspace_report.WorkspaceReportUrl)

        for workspace_dashboard in self.workspace_dashboard_list:
            print ("workspace dashboard > " + workspace_dashboard.WorkspaceName + " > " + workspace_dashboard.WorkspaceDashboardName + " > " + workspace_dashboard.WorkspaceDashboardUrl)
    
        for workspace_report_tab in self.workspace_report_tab_list:
            print ("workspace report tabs > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")

        for workspace_report_tab in self.workspace_report_tab_list:
            print ("workspace report duplicates tabs > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")
 
        for workspace_report_tab in self.workspace_report_tab_visual_errors_list:
            print ("workspace report tabs visual error > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")

        for workspace_dashboard in self.workspace_dashboard_visual_errors_list:
            print ("workspace dashboard visual error > " + workspace_dashboard.WorkspaceName + " > " + workspace_dashboard.WorkspaceDashboardName + " > " + workspace_dashboard.WorkspaceDashboardUrl + "\n")
    

    


    def saveData(self):

        self.logger.info("Saving the data to file started")

        current_output_file_name =  self.log_data_directory_path + "output_data_" + datetime.datetime.today().strftime("%Y%m%d_%H%M%S_") + self.current_run_guid + ".txt"
        
        with open(current_output_file_name, 'a') as output_file:
        
            for app in self.app_list:
                output_file.write("app > " + app.AppName + " > " + app.AppUrl + "\n")

            for workspace in self.workspae_list:
                output_file.write("workspace > " + workspace.WorkspaceName + " > " + workspace.WorkspaceUrl + "\n")

            for workspace_report in self.workspace_report_list:
                output_file.write("workspace report > " + workspace_report.WorkspaceName + " > " + workspace_report.WorkspaceReportName + " > " + workspace_report.WorkspaceReportUrl + "\n")

            for workspace_dashboard in self.workspace_dashboard_list:
                output_file.write("workspace dashboard > " + workspace_dashboard.WorkspaceName + " > " + workspace_dashboard.WorkspaceDashboardName + " > " + workspace_dashboard.WorkspaceDashboardUrl + "\n")

            for workspace_report_tab in self.workspace_report_tab_list:
                output_file.write("workspace report tabs > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")

            for workspace_report_tab in self.workspace_report_tab_duplicates_list:
                output_file.write("workspace report duplicate tabs > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")

            for workspace_report_tab in self.workspace_report_tab_visual_errors_list:
                output_file.write("workspace report tabs visual error > " + " > " + workspace_report_tab.WorkspaceName + " > " + workspace_report_tab.WorkspaceReportName + " > " + workspace_report_tab.WorkspaceReportUrl + " > " + workspace_report_tab.WorkspaceReportTabName + " > " + workspace_report_tab.WOrkspaceReportTabUrl + "\n")

            for workspace_dashboard in self.workspace_dashboard_visual_errors_list:
                output_file.write("workspace dashboard visual error > " + workspace_dashboard.WorkspaceName + " > " + workspace_dashboard.WorkspaceDashboardName + " > " + workspace_dashboard.WorkspaceDashboardUrl + "\n")

            
        self.logger.info("Saving the data to file done")



    def login(self):

        # go to the power bi main page
        self.browser.get(self.base_Url)

        try: # login

            self.logger.info("Trying to connect with username " + self.powerbi_user_name)

            # click sign in in main page
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//ul[@class='menu-secondary']//a[@ms.cmpnm='Sign in']"))).click()

            # fill user email in the first login page
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//input[@name='loginfmt']"))).send_keys(self.powerbi_user_email)

            # aprove user email/name and click next to go to the organization login
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//input[@class='btn btn-block btn-primary']"))).click()

            # fill user name in the second login page
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//input[@name='UserName']"))).send_keys(self.powerbi_user_name)

            # fill user password in the second login page
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//input[@name='Password']"))).send_keys(self.powerbi_user_password)

            # login to powerbi.com
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//div[@class='submitMargin']//span[@class='submit']"))).click()

            # choose to not remember user in the browser
            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//input[@class='btn btn-block' and @value='No']"))).click()

            # set the is_logged_in flag to true
            self.is_logged_in = True

            self.logger.info("Logging to powerbi.com succesfull")

        except TimeoutException:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("Timeout while trying to login, screenshot: " + error_screenshot_name)

        except:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("Other error while trying to login, screenshot: " + error_screenshot_name)





    def getApps(self):

        self.logger.info("Getting apps started")

        if self.is_logged_in == True:

            try: # get all apps addresses

                self.logger.info("Getting apps list started")

                # click Apps to go to the Apps tab
                WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//button[@title='Apps']//span[@class='btnLabel' and @localize='Apps_NavPaneTitle']"))).click()

                # get list of all app's names
                allAppsTitles = WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//html//section[@class='galleryContainer appsGallery']"))).find_elements_by_xpath("//li[@class='galleryItem unselectable']//h1")

                self.logger.info("Getting apps list done")
                self.logger.info("Getting all apps started")

                # prepare
                apps_page_path = self.browser.current_url
                main_window = self.browser.current_window_handle

                for app in allAppsTitles:

                    try: # get app page url

                        current_app_name = app.get_attribute("textContent").strip()

                        self.logger.info("Getting app <" + current_app_name + "> started")

                        # open new blank tab  
                        self.browser.execute_script("window.open('');")

                        # switch to new tab
                        self.browser.switch_to.window(self.browser.window_handles[1])

                        # go to the app page in the new tab
                        self.browser.get(apps_page_path)

                        # wait till the page will load and open - click - new app
                        WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//section[@class='galleryContainer appsGallery']//li[@aria-label='" + current_app_name + "']"))).click()

                        # get current page url and add to list
                        self.app_list.append(PowerbiApp(AppName = current_app_name, AppUrl = self.browser.current_url))

                        # close the current tab
                        self.browser.close()

                        # go to main tab
                        self.browser.switch_to_window(main_window)

                        self.logger.info("Getting app <" + current_app_name + "> done")

                    except:
                        error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                        self.logger.info("Error while getting app <" + current_app_name + "> started, screenshot: " + error_screenshot_name)

            except TimeoutException:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("Timed out while getting apps lists, screenshot: " + error_screenshot_name)

            except:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("Other error while getting apps lists, screenshot: " + error_screenshot_name)


            self.logger.info("Getting all apps done")

        else:
            self.logger.error("User not logged in")

        self.logger.info("Getting apps done")





    def getWorkspaces(self):

        self.logger.info("Getting workspaces started")

        if self.is_logged_in == True:

            try: # get all workspaces addresses

                self.logger.info("Getting workspaces list started")

                # go to main page
                self.browser.get(self.base_url_after_login)

                # click to expand workspaces list
                WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@title='Show/hide workspaces']"))).click()

                # wait till the list will open
                WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//group-list[@class='large']//header//span[@localize='NavigationPane_Groups_Workspaces_V2']")))

                # get all workspaces
                allWorkspaces = self.browser.find_elements_by_xpath("//ul//li[@ng-repeat='folder in $ctrl.appWorkspaces track by folder.uniqueId']//span[@class='workspaceName']")

                self.logger.info("Getting workspaces list done")
                self.logger.info("Getting all workspaces started")

                # prepare
                workspace_page_path = self.browser.current_url
                main_window = self.browser.current_window_handle

                # extract workspaces titles
                for workspace in allWorkspaces:

                    try: # get workspace url
                    
                        current_workspace_name = workspace.get_attribute("textContent").strip()

                        self.logger.info("Getting workspace <" + current_workspace_name + "> started")

                        # open new blank tab  
                        self.browser.execute_script("window.open('');")

                        # switch to new tab
                        self.browser.switch_to.window(self.browser.window_handles[1])

                        # go to the workspace page in the new tab
                        self.browser.get(workspace_page_path)

                        # click to expand workspaces list
                        WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//button[@title='Show/hide workspaces']"))).click()

                        # wait till the list will open
                        WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//group-list[@class='large']//header//span[@localize='NavigationPane_Groups_Workspaces_V2']")))

                        # wait till the page will load and open - click - new workspace
                        WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//li//button[@title='" + current_workspace_name + "']//span[@class='workspaceName']"))).click()

                        # get current page url and add to list
                        self.workspae_list.append(PowerbiWorkspace(WorkspaceName = current_workspace_name, WorkspaceUrl = self.browser.current_url))

                        # close the current tab
                        self.browser.close()

                        # go to main tab
                        self.browser.switch_to_window(main_window)

                        self.logger.info("Getting workspace <" + current_workspace_name + "> done")

                    except:
                        error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                        self.logger.error("Error while getting workspace " + current_workspace_name + ", screenshot: " + error_screenshot_name)

            except TimeoutException:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("Timed out while getting workspaces, screenshot: " + error_screenshot_name)
            except:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("Other error while getting workspaces, screenshot: " + error_screenshot_name)
        
            self.logger.info("Getting all workspaces done")

        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("User not logged in")
    
        self.logger.info("Getting workspaces done")








    def checkReportTabsVisualsErrors(self):
        
        self.logger.info("Getting reports tabs visual errors started")

        # check if there is any downloaded reports tabs
        if len(self.workspace_report_tab_list) > 0:
    
            # check if user is already logged in
            if self.is_logged_in == True:
        
                for workspace_report_tab in self.workspace_report_tab_list:

                    self.logger.info("Getting report tabs visual errors for: " + workspace_report_tab.WorkspaceReportTabName + " started")

                    # go to the specific report tab page
                    self.browser.get(workspace_report_tab.WOrkspaceReportTabUrl)

                    # wait till content will be loaded
                    WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@role='tab']")))

                    # wait extra seconds, try to find a better way here....
                    time.sleep(self.time_sleep_report_seconds)

                    # search for at least one error
                    visual_errors = self.browser.find_elements_by_xpath("//a[@class='errorSeeMore']")

                    if (len(visual_errors) > 0):
                        
                        # get screenshot with page that contains errors
                        screenshot_name = self.saveScreenshot(ScreenshotType.VisualError)
                        self.logger.info("Visual errors in report: " + workspace_report_tab.WorkspaceReportUrl + " , tab: " + workspace_report_tab.WorkspaceReportTabName + " , url: " + workspace_report_tab.WOrkspaceReportTabUrl + " , screnshot: " +  screenshot_name)
                        
                        # save erorr
                        self.workspace_report_tab_visual_errors_list.append(workspace_report_tab)

                    self.logger.info("Getting report tabs visual errors for: " + workspace_report_tab.WorkspaceReportTabName + " done")
            else:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.info("User not logged in, screenshot: " + error_screenshot_name)
        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.info("The workspace reports tabs list is empty. Get workspaces first, screenshot: " + error_screenshot_name)

        self.logger.info("Getting reports tabs visual errors done")









    def checkWorkspaceDashboardVisualsErrors(self):
        
        self.logger.info("Getting workspaces dashboards visual errors started")

        # check if there is any downloaded reports tabs
        if len(self.workspace_dashboard_list) > 0:
    
            # check if user is already logged in
            if self.is_logged_in == True:
        
                for workspace_dashboard in self.workspace_dashboard_list:

                    self.logger.info("Getting workspace dashboard visual errors for: " + workspace_dashboard.WorkspaceDashboardName + " started")

                    # go to the specific report tab page
                    self.browser.get(workspace_dashboard.WorkspaceDashboardUrl)

                    # wait till content will be loaded
                    WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@class='landingRootContent' and @id='dashboardLandingContainer']")))

                    # wait extra seconds, try to find a better way here....
                    time.sleep(self.time_sleep_report_seconds)

                    # search for at least one error
                    visual_errors = self.browser.find_elements_by_xpath("//div[@class='errorContainer']")

                    if (len(visual_errors) > 0):
                        
                        # get screenshot with page that contains errors
                        screenshot_name = self.saveScreenshot(ScreenshotType.VisualError)
                        self.logger.info("Visual errors in dashboard: " + workspace_dashboard.WorkspaceDashboardName  + " , url: " + workspace_dashboard.WorkspaceDashboardUrl + " , workspace: " + workspace_dashboard.WorkspaceName + " , screnshot: " +  screenshot_name)

                        # save error
                        self.workspace_dashboard_visual_errors_list.append(workspace_dashboard)

                    self.logger.info("Getting workspace dashboard visual errors for: " + workspace_dashboard.WorkspaceDashboardName + " done")

            else:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.info("User not logged in, screenshot: " + error_screenshot_name)

        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.info("The workspace dashboard list is empty. Get workspaces first, screenshot: " + error_screenshot_name)

        self.logger.info("Getting workspaces dashboards visual errors started")














    def getWorkspacesDashboards(self):

        self.logger.info("Getting workspaces dashboards started")

        if len(self.workspae_list) > 0:
    
            if self.is_logged_in == True:
        
                self.browser.get(self.base_url_after_login)

                try: # check errors in workspaces

                    for workspace in self.workspae_list:
  
                        current_workspace_name = workspace.WorkspaceName
                        current_workspace_url = workspace.WorkspaceUrl

                        self.logger.info("Getting dashboards for workspace " + current_workspace_name + " started")

                        try: # get workspace dashboards

                            self.logger.info("Getting dashboards lists for workspace " + current_workspace_name + " started")

                            ### iterate dashboards
                            current_workspace_dashboard_list_url = current_workspace_url + "/list/dashboards"

                            # go to workspace dashboard list
                            self.browser.get(current_workspace_dashboard_list_url)

                            # wait till the list of dashboard will be loaded
                            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@role='datagrid' or @class='dataSourceTiles']")))
                            time.sleep(self.time_sleep_normal_seconds) # additional wait while the previous one is not always working ....

                            # get all dashboard list
                            current_workspace_dashboards = self.browser.find_elements_by_xpath("//div[@class='row']//a")

                            self.logger.info("Getting dashboards lists for workspace " + current_workspace_name + " done")

                            # get all dashboard list - name + url 
                            for current_workspace_dashboard in current_workspace_dashboards:
                                current_workspace_dashboard_name = current_workspace_dashboard.get_attribute("textContent").strip()
                                current_workspace_dashboard_url = current_workspace_dashboard.get_attribute('href')

                                self.logger.info("Getting dashboards " + current_workspace_dashboard_name + " started")

                                self.workspace_dashboard_list.append(PowerbiWorkspaceDashboard(WorkspaceName = current_workspace_name, WorkspaceDashboardName = current_workspace_dashboard_name, WorkspaceDashboardUrl = current_workspace_dashboard_url))

                                self.logger.info("Getting dashboards " + current_workspace_dashboard_name + " done")
                                
                        except:
                            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                            self.logger.error("Error while getting worksapce dashboards list for " + current_workspace_name + ", screenshot: " + error_screenshot_name)


                        self.logger.info("Getting dashboards for workspace " + current_workspace_name + " done")

                except TimeoutException:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Timed out while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)
                except:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Other error while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)

            else:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("User not logged in" + ", screenshot: " + error_screenshot_name)
        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("The workspace list is empty. Get workspaces first" + ", screenshot: " + error_screenshot_name)

        self.logger.info("Getting workspaces dashboards done")





    def getWorkspacesReports(self):

        self.logger.info("Getting workspaces reports started")

        if len(self.workspae_list) > 0:
    
            if self.is_logged_in == True:
        
                self.browser.get(self.base_url_after_login)

                try: # check errors in workspaces

                    for workspace in self.workspae_list:
  
                        current_workspace_name = workspace.WorkspaceName
                        current_workspace_url = workspace.WorkspaceUrl

                        self.logger.info("Getting workspaces reports " + current_workspace_name + " started")

                        try: # get workspace reports
                            
                            self.logger.info("Getting workspaces reports list" + current_workspace_name + " started")

                            ### itearate reports
                            current_workspace_report_list_url = current_workspace_url + "/list/reports"

                            # go to workspace report list
                            self.browser.get(current_workspace_report_list_url)
                            
                            # wait till the list of reports will be loaded
                            WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@role='datagrid' or @class='dataSourceTiles']")))
                            time.sleep(self.time_sleep_normal_seconds) # additional wait while the previous one is not always working ....

                            # get all reports list
                            current_workspace_reports = self.browser.find_elements_by_xpath("//div[@class='row']//a")
                            
                            self.logger.info("Getting workspaces reports list" + current_workspace_name + " done")

                            # get all reports list - name + url 
                            for current_workspace_report in current_workspace_reports:
                                
                                current_workspace_report_name = current_workspace_report.get_attribute("textContent").strip()
                                current_workspace_report_url = current_workspace_report.get_attribute('href')
                                
                                self.logger.info("Getting report " + current_workspace_report_name + " started")

                                self.workspace_report_list.append(PowerbiWorkspaceReport(WorkspaceName = current_workspace_name, WorkspaceReportName = current_workspace_report_name, WorkspaceReportUrl = current_workspace_report_url))

                                self.logger.info("Getting report " + current_workspace_report_name + " done")

                        except:
                            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                            self.log("Error while getting worksapce reports list for " + current_workspace_name + ", screenshot: " + error_screenshot_name)
                        
                        self.logger.info("Getting workspaces reports " + current_workspace_name + " done")

                except TimeoutException:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Timed out while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)
                except:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Other error while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)

            else:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("User not logged in" + ", screenshot: " + error_screenshot_name)
        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("The workspace list is empty. Get workspaces first" + ", screenshot: " + error_screenshot_name)

        self.logger.info("Getting workspaces reports done")


    
    def getWorkspacesReportsTabs(self):

        self.logger.info("Getting workspaces reports tabs started")

        if len(self.workspae_list) > 0:
    
            if self.is_logged_in == True:

                self.browser.get(self.base_url_after_login)

                try: # check errors in workspaces

                    for workspace in self.workspae_list:
  
                        current_workspace_name = workspace.WorkspaceName

                        self.logger.info("Getting workspaces reports tabs for workspace " + current_workspace_name + " started")

                        try: # get workspace reports
                            
                            current_workspace_report_list = [x for x in self.workspace_report_list if x.WorkspaceName == current_workspace_name]

                            # get all reports list - name + url 
                            for current_workspace_report in current_workspace_report_list:
                                
                                current_workspace_report_name = current_workspace_report.WorkspaceReportName
                                current_workspace_report_url = current_workspace_report.WorkspaceReportUrl

                                self.logger.info("Getting workspaces reports tabs for report " + current_workspace_report_name + " started")

                                try: # get all tab
                                
                                    self.logger.info("Getting workspaces reports tabs list for report " + current_workspace_report_name + " started")

                                    # go to the single report - first page
                                    self.browser.get(current_workspace_report_url)

                                    # wait till the first report will be loaded to get all reports
                                    WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@role='tab']")))
                                    time.sleep(self.time_sleep_report_seconds) # additional wait while the previous one is not always working ....

                                    # get all tabs
                                    current_report_tabs = self.browser.find_elements_by_xpath("//div[@role='tab']")

                                    # prepare
                                    report_page_path = self.browser.current_url
                                    main_window = self.browser.current_window_handle

                                    current_report_tabs_names = []
                                    for report_tab in current_report_tabs:
                                        current_report_tabs_names.append(report_tab.get_attribute("textContent").strip())
 
                                    # check if there is more than one tab with given name in the report (duplicates)
                                    current_report_tab_name_count = collections.Counter(current_report_tabs_names)
                                    current_report_tab_name_count_single = {x : current_report_tab_name_count[x] for x in current_report_tab_name_count if current_report_tab_name_count[x] == 1 }
                                    current_report_tab_name_count_duplicates = {x : current_report_tab_name_count[x] for x in current_report_tab_name_count if current_report_tab_name_count[x] > 1 }

                                    if (len(current_report_tab_name_count_duplicates) > 0):

                                        for current_report_tab_name in list(current_report_tab_name_count_duplicates.keys()):

                                            self.workspace_report_tab_list.append(PowerbiWorkspaceReportTab(WorkspaceName = current_workspace_name, WorkspaceReportName = current_workspace_report_name, WorkspaceReportUrl = current_workspace_report_url, WorkspaceReportTabName = current_report_tab_name, WOrkspaceReportTabUrl = self.browser.current_url))


                                    self.logger.info("Getting workspaces reports tabs list for report " + current_workspace_report_name + " done")

                                    if (len(current_report_tab_name_count_single) > 0):
                                
                                        for current_report_tab_name in list(current_report_tab_name_count_single.keys()):

                                            self.logger.info("Getting workspaces reports tab " + current_report_tab_name + " started")

                                            try: # get report page tab url
                                            
                                                # open new blank tab  
                                                self.browser.execute_script("window.open('');")

                                                # switch to new tab
                                                self.browser.switch_to.window(self.browser.window_handles[1])

                                                # go to the app page in the new tab
                                                self.browser.get(report_page_path)

                                                # wait till the page will load and open - click - new app
                                                try:

                                                    # click on specific tab and wait till the tab will load
                                                    WebDriverWait(self.browser, self.page_load_timeout).until(EC.presence_of_element_located((By.XPATH, "//div[@role='tab']//div[@title='" + current_report_tab_name + "']"))).click()
                                                    time.sleep(self.time_sleep_report_seconds) # additional wait while the previous one is not always working ....

                                                    # get current page url and add to list
                                                    self.workspace_report_tab_list.append(PowerbiWorkspaceReportTab(WorkspaceName = current_workspace_name, WorkspaceReportName = current_workspace_report_name, WorkspaceReportUrl = current_workspace_report_url, WorkspaceReportTabName = current_report_tab_name, WOrkspaceReportTabUrl = self.browser.current_url))

                                                except:
                                                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                                                    self.logger.error("Error while getting workspace single tab workspace " + current_workspace_report_name + ", report " + current_workspace_report_name + ", report tab: " + current_report_tab_name + " , screenshot: none" )

                                                # close the current tab
                                                self.browser.close()

                                                # go to main tab
                                                self.browser.switch_to_window(main_window)

                                            except:
                                                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                                                self.logger.error("Error while getting workspace single tab url for workspace " + current_workspace_report_name + ", report " + current_workspace_report_name + ", report tab: " + current_report_tab_name + " , screenshot: none" )

                                            self.logger.info("Getting workspaces reports tab " + current_report_tab_name + " done")

                                except:
                                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                                    self.logger.error("Error while getting workspace single tab url for workspace " + current_workspace_report_name + ", report " + current_workspace_report_name  + " , screenshot: " + error_screenshot_name)

                                self.logger.info("Getting workspaces reports tabs for report " + current_workspace_report_name + " done")

                        except:
                            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                            self.logger.error("Error while getting worksapce reports list for " + current_workspace_name + ", screenshot: " + error_screenshot_name)
                        
                        self.logger.info("Getting workspaces reports tabs for workspace " + current_workspace_name + " done")

                except TimeoutException:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Timed out while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)
                except:
                    error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                    self.logger.error("Other error while checking errors in workspaces" + ", screenshot: " + error_screenshot_name)

            else:
                error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
                self.logger.error("User not logged in" + ", screenshot: " + error_screenshot_name)
        else:
            error_screenshot_name = self.saveScreenshot(ScreenshotType.CodeError)
            self.logger.error("The workspace list is empty. Get workspaces first" + ", screenshot: " + error_screenshot_name)

        self.logger.info("Getting workspaces reports tabs done")

