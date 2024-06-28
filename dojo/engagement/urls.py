from django.urls import re_path, path

from dojo.engagement import views

urlpatterns = [
    #  engagements and calendar
    re_path(r'^calendar$', views.engagement_calendar, name='calendar'),
    re_path(r'^calendar/engagements$', views.engagement_calendar, name='engagement_calendar'),
    re_path(r'^engagement$', views.engagements, {'view': 'active'}, name='engagement'),
    re_path(r'^engagements_all$', views.engagements_all, name='engagements_all'),
    re_path(r'^engagement/all$', views.engagements, {'view': 'all'}, name='all_engagements'),
    re_path(r'^engagement/active$', views.engagements, {'view': 'active'}, name='active_engagements'),
    re_path(r'^engagement/(?P<eid>\d+)$', views.ViewEngagement.as_view(),
        name='view_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/ics$', views.engagement_ics,
        name='engagement_ics'),
    re_path(r'^engagement/(?P<eid>\d+)/edit$', views.edit_engagement,
        name='edit_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/delete$', views.delete_engagement,
        name='delete_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/copy$', views.copy_engagement,
        name='copy_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/add_tests$', views.add_tests,
        name='add_tests'),
    re_path(
        r'^engagement/(?P<engagement_id>\d+)/import_scan_results$',
        views.ImportScanResultsView.as_view(),
        name='import_scan_results'),
    re_path(r'^engagement/(?P<eid>\d+)/close$', views.close_eng,
        name='close_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/reopen$', views.reopen_eng,
        name='reopen_engagement'),
    re_path(r'^engagement/(?P<eid>\d+)/complete_checklist$',
        views.complete_checklist, name='complete_checklist'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/add$',
        views.add_risk_acceptance, name='add_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/add/(?P<fid>\d+)$',
        views.add_risk_acceptance, name='add_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/add_transfer_finding/add/(?P<fid>\d+)$',
            views.add_transfer_finding, name="add_transfer_finding"),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)$',
        views.view_risk_acceptance, name='view_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/edit$',
        views.edit_risk_acceptance, name='edit_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/expire$',
        views.expire_risk_acceptance, name='expire_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/accept$',
        views.accept_risk_acceptance, name='accept_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/reinstate$',
        views.reinstate_risk_acceptance, name='reinstate_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/delete$',
        views.delete_risk_acceptance, name='delete_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/risk_acceptance/(?P<raid>\d+)/download$',
        views.download_risk_acceptance, name='download_risk_acceptance'),
    re_path(r'^engagement/(?P<eid>\d+)/threatmodel$', views.view_threatmodel,
        name='view_threatmodel'),
    re_path(r'^engagement/(?P<eid>\d+)/threatmodel/upload$',
        views.upload_threatmodel, name='upload_threatmodel'),
    re_path(r'^engagement/csv_export$',
        views.csv_export, name='engagement_csv_export'),
    re_path(r'^engagement/excel_export$',
        views.excel_export, name='engagement_excel_export'),
]
