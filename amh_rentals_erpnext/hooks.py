from . import __version__ as app_version  # noqa

app_name = "amh_rentals_erpnext"
app_title = "AMH Rentals - ERPNext"
app_publisher = "Fahim Ali Zain"
app_description = "ERPNext Customizations for AMH Rentals"
app_icon = "octicon octicon-file-directory"
app_color = "yellow"
app_email = "fahimalizain@gmail.com"
app_license = "MIT"

fixtures = [{
    "doctype": "Custom Field",
    "filters": [["name", "in", [
            "Branch-warehouse",
            "Stock Settings-rented_warehouse"
            ]]]
}]

doc_events = {
    "Branch": {
        "on_update": "amh_rentals_erpnext.doc_events.branch.on_update"
    }
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/amh_rentals_erpnext/css/amh_rentals_erpnext.css"
# app_include_js = "/assets/amh_rentals_erpnext/js/amh_rentals_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/amh_rentals_erpnext/css/amh_rentals_erpnext.css"
# web_include_js = "/assets/amh_rentals_erpnext/js/amh_rentals_erpnext.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "amh_rentals_erpnext/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#    "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "amh_rentals_erpnext.install.before_install"
# after_install = "amh_rentals_erpnext.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "amh_rentals_erpnext.uninstall.before_uninstall"
# after_uninstall = "amh_rentals_erpnext.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "amh_rentals_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	 "*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#    }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"amh_rentals_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"amh_rentals_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"amh_rentals_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"amh_rentals_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"amh_rentals_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "amh_rentals_erpnext.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "amh_rentals_erpnext.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "amh_rentals_erpnext.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"amh_rentals_erpnext.auth.validate"
# ]
