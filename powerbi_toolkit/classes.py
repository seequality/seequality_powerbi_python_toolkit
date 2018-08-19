from dataclasses import dataclass
from enum import Enum

@dataclass
class PowerbiApp(object):
    AppName: str
    AppUrl: str

@dataclass
class PowerbiWorkspace(object):
    WorkspaceName: str
    WorkspaceUrl: str

@dataclass
class PowerbiWorkspaceReport(object):
    WorkspaceName: str
    WorkspaceReportName: str
    WorkspaceReportUrl: str

@dataclass
class PowerbiWorkspaceDashboard(object):
    WorkspaceName: str
    WorkspaceDashboardName: str
    WorkspaceDashboardUrl: str

@dataclass
class PowerbiWorkspaceReportTab(object):
    WorkspaceName: str
    WorkspaceReportName: str
    WorkspaceReportUrl: str
    WorkspaceReportTabName: str
    WOrkspaceReportTabUrl: str

class ScreenshotType(Enum):
    CodeError = "codeerror"
    VisualError = "visualerror"
