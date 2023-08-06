import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.organization_addon_billing_period import OrganizationAddonBillingPeriod
from ..models.organization_invoice_billing_period import OrganizationInvoiceBillingPeriod
from ..models.organization_plan import OrganizationPlan
from ..models.organization_support_tier import OrganizationSupportTier
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aws_info import AwsInfo
    from ..models.billing_info import BillingInfo
    from ..models.google_info import GoogleInfo
    from ..models.google_storage_info import GoogleStorageInfo
    from ..models.looker_info import LookerInfo
    from ..models.pagerduty_info import PagerdutyInfo
    from ..models.rtc_info import RtcInfo
    from ..models.slack_info import SlackInfo
    from ..models.stripe_info import StripeInfo
    from ..models.user_teleop_configuration import UserTeleopConfiguration
    from ..models.webhooks_info import WebhooksInfo


T = TypeVar("T", bound="Organization")


@attr.s(auto_attribs=True)
class Organization:
    """
    Attributes:
        plan (OrganizationPlan):
        name (str):
        industry (str):
        website (str):
        address_line_1 (str):
        address_line_2 (str):
        city (str):
        state (str):
        postal_code (str):
        country (str):
        addon_billing_period (OrganizationAddonBillingPeriod):
        invoice_billing_period (OrganizationInvoiceBillingPeriod):
        enabled (Union[Unset, bool]):
        pagerduty_info (Union[Unset, PagerdutyInfo]):
        slack_info (Union[Unset, SlackInfo]):
        google_info (Union[Unset, GoogleInfo]):
        webhooks_info (Union[Unset, WebhooksInfo]):
        aws_info (Union[Unset, AwsInfo]):
        google_storage_info (Union[Unset, GoogleStorageInfo]):
        looker_info (Union[Unset, LookerInfo]):
        stripe_info (Union[Unset, StripeInfo]):
        rtc_info (Union[Unset, RtcInfo]):
        teleop_configuration (Union[Unset, UserTeleopConfiguration]):
        analytics_enabled (Union[Unset, None, datetime.datetime]):
        data_export_enabled (Union[Unset, None, datetime.datetime]):
        advanced_configuration_enabled (Union[Unset, None, datetime.datetime]):
        customer_portal_enabled (Union[Unset, None, datetime.datetime]):
        stripe_billing_enabled (Union[Unset, bool]):
        stripe_subscription_enabled (Union[Unset, bool]):
        billing_info (Union[Unset, BillingInfo]):
        s_3_export_enabled (Union[Unset, bool]):
        blob_data_enabled (Union[Unset, bool]):
        white_label_enabled (Union[Unset, bool]):
        viewer_3_d_enabled (Union[Unset, bool]):
        adapters_enabled (Union[Unset, bool]):
        white_label_css (Union[Unset, None, str]):
        demo_mode_enabled (Union[Unset, bool]):
        teleop_share_enabled (Union[Unset, bool]):
        bill_estimate_enabled (Union[Unset, bool]):
        data_retention_enabled (Union[Unset, None, datetime.datetime]):
        days_data_retained (Union[Unset, int]):
        max_chunk_request_limit (Union[Unset, int]):
        support_enabled (Union[Unset, None, datetime.datetime]):
        support_tier (Union[Unset, OrganizationSupportTier]):
        trial_period_end (Optional[datetime.datetime]):
        external_id (Union[Unset, str]):
        chargebee_id (Optional[str]):
        totango_id (Optional[str]):
        custom_tos (Union[Unset, bool]):
        teleop_enabled (Union[Unset, None, datetime.datetime]):
        observability_enabled (Union[Unset, None, datetime.datetime]):
        share_enabled (Union[Unset, None, datetime.datetime]):
        annotations_enabled (Union[Unset, None, datetime.datetime]):
        diagnostics_enabled (Union[Unset, None, datetime.datetime]):
        ssh_enabled (Union[Unset, None, datetime.datetime]):
        spot_enabled (Union[Unset, None, datetime.datetime]):
        file_storage_enabled (Union[Unset, bool]):
        role_viewer_enabled (Union[Unset, bool]):
        teams_enabled (Union[Unset, bool]):
        schedules_enabled (Union[Unset, bool]):
        paging_enabled (Union[Unset, bool]):
        stateful_events_enabled (Union[Unset, bool]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    plan: OrganizationPlan
    name: str
    industry: str
    website: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    country: str
    addon_billing_period: OrganizationAddonBillingPeriod
    invoice_billing_period: OrganizationInvoiceBillingPeriod
    trial_period_end: Optional[datetime.datetime]
    chargebee_id: Optional[str]
    totango_id: Optional[str]
    enabled: Union[Unset, bool] = UNSET
    pagerduty_info: Union[Unset, "PagerdutyInfo"] = UNSET
    slack_info: Union[Unset, "SlackInfo"] = UNSET
    google_info: Union[Unset, "GoogleInfo"] = UNSET
    webhooks_info: Union[Unset, "WebhooksInfo"] = UNSET
    aws_info: Union[Unset, "AwsInfo"] = UNSET
    google_storage_info: Union[Unset, "GoogleStorageInfo"] = UNSET
    looker_info: Union[Unset, "LookerInfo"] = UNSET
    stripe_info: Union[Unset, "StripeInfo"] = UNSET
    rtc_info: Union[Unset, "RtcInfo"] = UNSET
    teleop_configuration: Union[Unset, "UserTeleopConfiguration"] = UNSET
    analytics_enabled: Union[Unset, None, datetime.datetime] = UNSET
    data_export_enabled: Union[Unset, None, datetime.datetime] = UNSET
    advanced_configuration_enabled: Union[Unset, None, datetime.datetime] = UNSET
    customer_portal_enabled: Union[Unset, None, datetime.datetime] = UNSET
    stripe_billing_enabled: Union[Unset, bool] = UNSET
    stripe_subscription_enabled: Union[Unset, bool] = UNSET
    billing_info: Union[Unset, "BillingInfo"] = UNSET
    s_3_export_enabled: Union[Unset, bool] = UNSET
    blob_data_enabled: Union[Unset, bool] = UNSET
    white_label_enabled: Union[Unset, bool] = UNSET
    viewer_3_d_enabled: Union[Unset, bool] = UNSET
    adapters_enabled: Union[Unset, bool] = UNSET
    white_label_css: Union[Unset, None, str] = UNSET
    demo_mode_enabled: Union[Unset, bool] = UNSET
    teleop_share_enabled: Union[Unset, bool] = UNSET
    bill_estimate_enabled: Union[Unset, bool] = UNSET
    data_retention_enabled: Union[Unset, None, datetime.datetime] = UNSET
    days_data_retained: Union[Unset, int] = UNSET
    max_chunk_request_limit: Union[Unset, int] = UNSET
    support_enabled: Union[Unset, None, datetime.datetime] = UNSET
    support_tier: Union[Unset, OrganizationSupportTier] = UNSET
    external_id: Union[Unset, str] = UNSET
    custom_tos: Union[Unset, bool] = UNSET
    teleop_enabled: Union[Unset, None, datetime.datetime] = UNSET
    observability_enabled: Union[Unset, None, datetime.datetime] = UNSET
    share_enabled: Union[Unset, None, datetime.datetime] = UNSET
    annotations_enabled: Union[Unset, None, datetime.datetime] = UNSET
    diagnostics_enabled: Union[Unset, None, datetime.datetime] = UNSET
    ssh_enabled: Union[Unset, None, datetime.datetime] = UNSET
    spot_enabled: Union[Unset, None, datetime.datetime] = UNSET
    file_storage_enabled: Union[Unset, bool] = UNSET
    role_viewer_enabled: Union[Unset, bool] = UNSET
    teams_enabled: Union[Unset, bool] = UNSET
    schedules_enabled: Union[Unset, bool] = UNSET
    paging_enabled: Union[Unset, bool] = UNSET
    stateful_events_enabled: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        plan = self.plan.value

        name = self.name
        industry = self.industry
        website = self.website
        address_line_1 = self.address_line_1
        address_line_2 = self.address_line_2
        city = self.city
        state = self.state
        postal_code = self.postal_code
        country = self.country
        addon_billing_period = self.addon_billing_period.value

        invoice_billing_period = self.invoice_billing_period.value

        enabled = self.enabled
        pagerduty_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagerduty_info, Unset):
            pagerduty_info = self.pagerduty_info.to_dict()

        slack_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.slack_info, Unset):
            slack_info = self.slack_info.to_dict()

        google_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.google_info, Unset):
            google_info = self.google_info.to_dict()

        webhooks_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.webhooks_info, Unset):
            webhooks_info = self.webhooks_info.to_dict()

        aws_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.aws_info, Unset):
            aws_info = self.aws_info.to_dict()

        google_storage_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.google_storage_info, Unset):
            google_storage_info = self.google_storage_info.to_dict()

        looker_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.looker_info, Unset):
            looker_info = self.looker_info.to_dict()

        stripe_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stripe_info, Unset):
            stripe_info = self.stripe_info.to_dict()

        rtc_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.rtc_info, Unset):
            rtc_info = self.rtc_info.to_dict()

        teleop_configuration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.teleop_configuration, Unset):
            teleop_configuration = self.teleop_configuration.to_dict()

        analytics_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.analytics_enabled, Unset):
            analytics_enabled = self.analytics_enabled.isoformat() if self.analytics_enabled else None

        data_export_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.data_export_enabled, Unset):
            data_export_enabled = self.data_export_enabled.isoformat() if self.data_export_enabled else None

        advanced_configuration_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.advanced_configuration_enabled, Unset):
            advanced_configuration_enabled = (
                self.advanced_configuration_enabled.isoformat() if self.advanced_configuration_enabled else None
            )

        customer_portal_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.customer_portal_enabled, Unset):
            customer_portal_enabled = self.customer_portal_enabled.isoformat() if self.customer_portal_enabled else None

        stripe_billing_enabled = self.stripe_billing_enabled
        stripe_subscription_enabled = self.stripe_subscription_enabled
        billing_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.billing_info, Unset):
            billing_info = self.billing_info.to_dict()

        s_3_export_enabled = self.s_3_export_enabled
        blob_data_enabled = self.blob_data_enabled
        white_label_enabled = self.white_label_enabled
        viewer_3_d_enabled = self.viewer_3_d_enabled
        adapters_enabled = self.adapters_enabled
        white_label_css = self.white_label_css
        demo_mode_enabled = self.demo_mode_enabled
        teleop_share_enabled = self.teleop_share_enabled
        bill_estimate_enabled = self.bill_estimate_enabled
        data_retention_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.data_retention_enabled, Unset):
            data_retention_enabled = self.data_retention_enabled.isoformat() if self.data_retention_enabled else None

        days_data_retained = self.days_data_retained
        max_chunk_request_limit = self.max_chunk_request_limit
        support_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.support_enabled, Unset):
            support_enabled = self.support_enabled.isoformat() if self.support_enabled else None

        support_tier: Union[Unset, str] = UNSET
        if not isinstance(self.support_tier, Unset):
            support_tier = self.support_tier.value

        trial_period_end = self.trial_period_end.isoformat() if self.trial_period_end else None

        external_id = self.external_id
        chargebee_id = self.chargebee_id
        totango_id = self.totango_id
        custom_tos = self.custom_tos
        teleop_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.teleop_enabled, Unset):
            teleop_enabled = self.teleop_enabled.isoformat() if self.teleop_enabled else None

        observability_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.observability_enabled, Unset):
            observability_enabled = self.observability_enabled.isoformat() if self.observability_enabled else None

        share_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.share_enabled, Unset):
            share_enabled = self.share_enabled.isoformat() if self.share_enabled else None

        annotations_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.annotations_enabled, Unset):
            annotations_enabled = self.annotations_enabled.isoformat() if self.annotations_enabled else None

        diagnostics_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.diagnostics_enabled, Unset):
            diagnostics_enabled = self.diagnostics_enabled.isoformat() if self.diagnostics_enabled else None

        ssh_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.ssh_enabled, Unset):
            ssh_enabled = self.ssh_enabled.isoformat() if self.ssh_enabled else None

        spot_enabled: Union[Unset, None, str] = UNSET
        if not isinstance(self.spot_enabled, Unset):
            spot_enabled = self.spot_enabled.isoformat() if self.spot_enabled else None

        file_storage_enabled = self.file_storage_enabled
        role_viewer_enabled = self.role_viewer_enabled
        teams_enabled = self.teams_enabled
        schedules_enabled = self.schedules_enabled
        paging_enabled = self.paging_enabled
        stateful_events_enabled = self.stateful_events_enabled
        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan": plan,
                "name": name,
                "industry": industry,
                "website": website,
                "addressLine1": address_line_1,
                "addressLine2": address_line_2,
                "city": city,
                "state": state,
                "postalCode": postal_code,
                "country": country,
                "addonBillingPeriod": addon_billing_period,
                "invoiceBillingPeriod": invoice_billing_period,
                "trialPeriodEnd": trial_period_end,
                "chargebeeId": chargebee_id,
                "totangoId": totango_id,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if pagerduty_info is not UNSET:
            field_dict["pagerdutyInfo"] = pagerduty_info
        if slack_info is not UNSET:
            field_dict["slackInfo"] = slack_info
        if google_info is not UNSET:
            field_dict["googleInfo"] = google_info
        if webhooks_info is not UNSET:
            field_dict["webhooksInfo"] = webhooks_info
        if aws_info is not UNSET:
            field_dict["awsInfo"] = aws_info
        if google_storage_info is not UNSET:
            field_dict["googleStorageInfo"] = google_storage_info
        if looker_info is not UNSET:
            field_dict["lookerInfo"] = looker_info
        if stripe_info is not UNSET:
            field_dict["stripeInfo"] = stripe_info
        if rtc_info is not UNSET:
            field_dict["rtcInfo"] = rtc_info
        if teleop_configuration is not UNSET:
            field_dict["teleopConfiguration"] = teleop_configuration
        if analytics_enabled is not UNSET:
            field_dict["analyticsEnabled"] = analytics_enabled
        if data_export_enabled is not UNSET:
            field_dict["dataExportEnabled"] = data_export_enabled
        if advanced_configuration_enabled is not UNSET:
            field_dict["advancedConfigurationEnabled"] = advanced_configuration_enabled
        if customer_portal_enabled is not UNSET:
            field_dict["customerPortalEnabled"] = customer_portal_enabled
        if stripe_billing_enabled is not UNSET:
            field_dict["stripeBillingEnabled"] = stripe_billing_enabled
        if stripe_subscription_enabled is not UNSET:
            field_dict["stripeSubscriptionEnabled"] = stripe_subscription_enabled
        if billing_info is not UNSET:
            field_dict["billingInfo"] = billing_info
        if s_3_export_enabled is not UNSET:
            field_dict["s3ExportEnabled"] = s_3_export_enabled
        if blob_data_enabled is not UNSET:
            field_dict["blobDataEnabled"] = blob_data_enabled
        if white_label_enabled is not UNSET:
            field_dict["whiteLabelEnabled"] = white_label_enabled
        if viewer_3_d_enabled is not UNSET:
            field_dict["viewer3dEnabled"] = viewer_3_d_enabled
        if adapters_enabled is not UNSET:
            field_dict["adaptersEnabled"] = adapters_enabled
        if white_label_css is not UNSET:
            field_dict["whiteLabelCSS"] = white_label_css
        if demo_mode_enabled is not UNSET:
            field_dict["demoModeEnabled"] = demo_mode_enabled
        if teleop_share_enabled is not UNSET:
            field_dict["teleopShareEnabled"] = teleop_share_enabled
        if bill_estimate_enabled is not UNSET:
            field_dict["billEstimateEnabled"] = bill_estimate_enabled
        if data_retention_enabled is not UNSET:
            field_dict["dataRetentionEnabled"] = data_retention_enabled
        if days_data_retained is not UNSET:
            field_dict["daysDataRetained"] = days_data_retained
        if max_chunk_request_limit is not UNSET:
            field_dict["maxChunkRequestLimit"] = max_chunk_request_limit
        if support_enabled is not UNSET:
            field_dict["supportEnabled"] = support_enabled
        if support_tier is not UNSET:
            field_dict["supportTier"] = support_tier
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if custom_tos is not UNSET:
            field_dict["customTos"] = custom_tos
        if teleop_enabled is not UNSET:
            field_dict["teleopEnabled"] = teleop_enabled
        if observability_enabled is not UNSET:
            field_dict["observabilityEnabled"] = observability_enabled
        if share_enabled is not UNSET:
            field_dict["shareEnabled"] = share_enabled
        if annotations_enabled is not UNSET:
            field_dict["annotationsEnabled"] = annotations_enabled
        if diagnostics_enabled is not UNSET:
            field_dict["diagnosticsEnabled"] = diagnostics_enabled
        if ssh_enabled is not UNSET:
            field_dict["sshEnabled"] = ssh_enabled
        if spot_enabled is not UNSET:
            field_dict["spotEnabled"] = spot_enabled
        if file_storage_enabled is not UNSET:
            field_dict["fileStorageEnabled"] = file_storage_enabled
        if role_viewer_enabled is not UNSET:
            field_dict["roleViewerEnabled"] = role_viewer_enabled
        if teams_enabled is not UNSET:
            field_dict["teamsEnabled"] = teams_enabled
        if schedules_enabled is not UNSET:
            field_dict["schedulesEnabled"] = schedules_enabled
        if paging_enabled is not UNSET:
            field_dict["pagingEnabled"] = paging_enabled
        if stateful_events_enabled is not UNSET:
            field_dict["statefulEventsEnabled"] = stateful_events_enabled
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.aws_info import AwsInfo
        from ..models.billing_info import BillingInfo
        from ..models.google_info import GoogleInfo
        from ..models.google_storage_info import GoogleStorageInfo
        from ..models.looker_info import LookerInfo
        from ..models.pagerduty_info import PagerdutyInfo
        from ..models.rtc_info import RtcInfo
        from ..models.slack_info import SlackInfo
        from ..models.stripe_info import StripeInfo
        from ..models.user_teleop_configuration import UserTeleopConfiguration
        from ..models.webhooks_info import WebhooksInfo

        d = src_dict.copy()
        plan = OrganizationPlan(d.pop("plan"))

        name = d.pop("name")

        industry = d.pop("industry")

        website = d.pop("website")

        address_line_1 = d.pop("addressLine1")

        address_line_2 = d.pop("addressLine2")

        city = d.pop("city")

        state = d.pop("state")

        postal_code = d.pop("postalCode")

        country = d.pop("country")

        addon_billing_period = OrganizationAddonBillingPeriod(d.pop("addonBillingPeriod"))

        invoice_billing_period = OrganizationInvoiceBillingPeriod(d.pop("invoiceBillingPeriod"))

        enabled = d.pop("enabled", UNSET)

        _pagerduty_info = d.pop("pagerdutyInfo", UNSET)
        pagerduty_info: Union[Unset, PagerdutyInfo]
        if isinstance(_pagerduty_info, Unset):
            pagerduty_info = UNSET
        else:
            pagerduty_info = PagerdutyInfo.from_dict(_pagerduty_info)

        _slack_info = d.pop("slackInfo", UNSET)
        slack_info: Union[Unset, SlackInfo]
        if isinstance(_slack_info, Unset):
            slack_info = UNSET
        else:
            slack_info = SlackInfo.from_dict(_slack_info)

        _google_info = d.pop("googleInfo", UNSET)
        google_info: Union[Unset, GoogleInfo]
        if isinstance(_google_info, Unset):
            google_info = UNSET
        else:
            google_info = GoogleInfo.from_dict(_google_info)

        _webhooks_info = d.pop("webhooksInfo", UNSET)
        webhooks_info: Union[Unset, WebhooksInfo]
        if isinstance(_webhooks_info, Unset):
            webhooks_info = UNSET
        else:
            webhooks_info = WebhooksInfo.from_dict(_webhooks_info)

        _aws_info = d.pop("awsInfo", UNSET)
        aws_info: Union[Unset, AwsInfo]
        if isinstance(_aws_info, Unset):
            aws_info = UNSET
        else:
            aws_info = AwsInfo.from_dict(_aws_info)

        _google_storage_info = d.pop("googleStorageInfo", UNSET)
        google_storage_info: Union[Unset, GoogleStorageInfo]
        if isinstance(_google_storage_info, Unset):
            google_storage_info = UNSET
        else:
            google_storage_info = GoogleStorageInfo.from_dict(_google_storage_info)

        _looker_info = d.pop("lookerInfo", UNSET)
        looker_info: Union[Unset, LookerInfo]
        if isinstance(_looker_info, Unset):
            looker_info = UNSET
        else:
            looker_info = LookerInfo.from_dict(_looker_info)

        _stripe_info = d.pop("stripeInfo", UNSET)
        stripe_info: Union[Unset, StripeInfo]
        if isinstance(_stripe_info, Unset):
            stripe_info = UNSET
        else:
            stripe_info = StripeInfo.from_dict(_stripe_info)

        _rtc_info = d.pop("rtcInfo", UNSET)
        rtc_info: Union[Unset, RtcInfo]
        if isinstance(_rtc_info, Unset):
            rtc_info = UNSET
        else:
            rtc_info = RtcInfo.from_dict(_rtc_info)

        _teleop_configuration = d.pop("teleopConfiguration", UNSET)
        teleop_configuration: Union[Unset, UserTeleopConfiguration]
        if isinstance(_teleop_configuration, Unset):
            teleop_configuration = UNSET
        else:
            teleop_configuration = UserTeleopConfiguration.from_dict(_teleop_configuration)

        _analytics_enabled = d.pop("analyticsEnabled", UNSET)
        analytics_enabled: Union[Unset, None, datetime.datetime]
        if _analytics_enabled is None:
            analytics_enabled = None
        elif isinstance(_analytics_enabled, Unset):
            analytics_enabled = UNSET
        else:
            analytics_enabled = isoparse(_analytics_enabled)

        _data_export_enabled = d.pop("dataExportEnabled", UNSET)
        data_export_enabled: Union[Unset, None, datetime.datetime]
        if _data_export_enabled is None:
            data_export_enabled = None
        elif isinstance(_data_export_enabled, Unset):
            data_export_enabled = UNSET
        else:
            data_export_enabled = isoparse(_data_export_enabled)

        _advanced_configuration_enabled = d.pop("advancedConfigurationEnabled", UNSET)
        advanced_configuration_enabled: Union[Unset, None, datetime.datetime]
        if _advanced_configuration_enabled is None:
            advanced_configuration_enabled = None
        elif isinstance(_advanced_configuration_enabled, Unset):
            advanced_configuration_enabled = UNSET
        else:
            advanced_configuration_enabled = isoparse(_advanced_configuration_enabled)

        _customer_portal_enabled = d.pop("customerPortalEnabled", UNSET)
        customer_portal_enabled: Union[Unset, None, datetime.datetime]
        if _customer_portal_enabled is None:
            customer_portal_enabled = None
        elif isinstance(_customer_portal_enabled, Unset):
            customer_portal_enabled = UNSET
        else:
            customer_portal_enabled = isoparse(_customer_portal_enabled)

        stripe_billing_enabled = d.pop("stripeBillingEnabled", UNSET)

        stripe_subscription_enabled = d.pop("stripeSubscriptionEnabled", UNSET)

        _billing_info = d.pop("billingInfo", UNSET)
        billing_info: Union[Unset, BillingInfo]
        if isinstance(_billing_info, Unset):
            billing_info = UNSET
        else:
            billing_info = BillingInfo.from_dict(_billing_info)

        s_3_export_enabled = d.pop("s3ExportEnabled", UNSET)

        blob_data_enabled = d.pop("blobDataEnabled", UNSET)

        white_label_enabled = d.pop("whiteLabelEnabled", UNSET)

        viewer_3_d_enabled = d.pop("viewer3dEnabled", UNSET)

        adapters_enabled = d.pop("adaptersEnabled", UNSET)

        white_label_css = d.pop("whiteLabelCSS", UNSET)

        demo_mode_enabled = d.pop("demoModeEnabled", UNSET)

        teleop_share_enabled = d.pop("teleopShareEnabled", UNSET)

        bill_estimate_enabled = d.pop("billEstimateEnabled", UNSET)

        _data_retention_enabled = d.pop("dataRetentionEnabled", UNSET)
        data_retention_enabled: Union[Unset, None, datetime.datetime]
        if _data_retention_enabled is None:
            data_retention_enabled = None
        elif isinstance(_data_retention_enabled, Unset):
            data_retention_enabled = UNSET
        else:
            data_retention_enabled = isoparse(_data_retention_enabled)

        days_data_retained = d.pop("daysDataRetained", UNSET)

        max_chunk_request_limit = d.pop("maxChunkRequestLimit", UNSET)

        _support_enabled = d.pop("supportEnabled", UNSET)
        support_enabled: Union[Unset, None, datetime.datetime]
        if _support_enabled is None:
            support_enabled = None
        elif isinstance(_support_enabled, Unset):
            support_enabled = UNSET
        else:
            support_enabled = isoparse(_support_enabled)

        _support_tier = d.pop("supportTier", UNSET)
        support_tier: Union[Unset, OrganizationSupportTier]
        if isinstance(_support_tier, Unset):
            support_tier = UNSET
        else:
            support_tier = OrganizationSupportTier(_support_tier)

        _trial_period_end = d.pop("trialPeriodEnd")
        trial_period_end: Optional[datetime.datetime]
        if _trial_period_end is None:
            trial_period_end = None
        else:
            trial_period_end = isoparse(_trial_period_end)

        external_id = d.pop("externalId", UNSET)

        chargebee_id = d.pop("chargebeeId")

        totango_id = d.pop("totangoId")

        custom_tos = d.pop("customTos", UNSET)

        _teleop_enabled = d.pop("teleopEnabled", UNSET)
        teleop_enabled: Union[Unset, None, datetime.datetime]
        if _teleop_enabled is None:
            teleop_enabled = None
        elif isinstance(_teleop_enabled, Unset):
            teleop_enabled = UNSET
        else:
            teleop_enabled = isoparse(_teleop_enabled)

        _observability_enabled = d.pop("observabilityEnabled", UNSET)
        observability_enabled: Union[Unset, None, datetime.datetime]
        if _observability_enabled is None:
            observability_enabled = None
        elif isinstance(_observability_enabled, Unset):
            observability_enabled = UNSET
        else:
            observability_enabled = isoparse(_observability_enabled)

        _share_enabled = d.pop("shareEnabled", UNSET)
        share_enabled: Union[Unset, None, datetime.datetime]
        if _share_enabled is None:
            share_enabled = None
        elif isinstance(_share_enabled, Unset):
            share_enabled = UNSET
        else:
            share_enabled = isoparse(_share_enabled)

        _annotations_enabled = d.pop("annotationsEnabled", UNSET)
        annotations_enabled: Union[Unset, None, datetime.datetime]
        if _annotations_enabled is None:
            annotations_enabled = None
        elif isinstance(_annotations_enabled, Unset):
            annotations_enabled = UNSET
        else:
            annotations_enabled = isoparse(_annotations_enabled)

        _diagnostics_enabled = d.pop("diagnosticsEnabled", UNSET)
        diagnostics_enabled: Union[Unset, None, datetime.datetime]
        if _diagnostics_enabled is None:
            diagnostics_enabled = None
        elif isinstance(_diagnostics_enabled, Unset):
            diagnostics_enabled = UNSET
        else:
            diagnostics_enabled = isoparse(_diagnostics_enabled)

        _ssh_enabled = d.pop("sshEnabled", UNSET)
        ssh_enabled: Union[Unset, None, datetime.datetime]
        if _ssh_enabled is None:
            ssh_enabled = None
        elif isinstance(_ssh_enabled, Unset):
            ssh_enabled = UNSET
        else:
            ssh_enabled = isoparse(_ssh_enabled)

        _spot_enabled = d.pop("spotEnabled", UNSET)
        spot_enabled: Union[Unset, None, datetime.datetime]
        if _spot_enabled is None:
            spot_enabled = None
        elif isinstance(_spot_enabled, Unset):
            spot_enabled = UNSET
        else:
            spot_enabled = isoparse(_spot_enabled)

        file_storage_enabled = d.pop("fileStorageEnabled", UNSET)

        role_viewer_enabled = d.pop("roleViewerEnabled", UNSET)

        teams_enabled = d.pop("teamsEnabled", UNSET)

        schedules_enabled = d.pop("schedulesEnabled", UNSET)

        paging_enabled = d.pop("pagingEnabled", UNSET)

        stateful_events_enabled = d.pop("statefulEventsEnabled", UNSET)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        organization = cls(
            plan=plan,
            name=name,
            industry=industry,
            website=website,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            addon_billing_period=addon_billing_period,
            invoice_billing_period=invoice_billing_period,
            enabled=enabled,
            pagerduty_info=pagerduty_info,
            slack_info=slack_info,
            google_info=google_info,
            webhooks_info=webhooks_info,
            aws_info=aws_info,
            google_storage_info=google_storage_info,
            looker_info=looker_info,
            stripe_info=stripe_info,
            rtc_info=rtc_info,
            teleop_configuration=teleop_configuration,
            analytics_enabled=analytics_enabled,
            data_export_enabled=data_export_enabled,
            advanced_configuration_enabled=advanced_configuration_enabled,
            customer_portal_enabled=customer_portal_enabled,
            stripe_billing_enabled=stripe_billing_enabled,
            stripe_subscription_enabled=stripe_subscription_enabled,
            billing_info=billing_info,
            s_3_export_enabled=s_3_export_enabled,
            blob_data_enabled=blob_data_enabled,
            white_label_enabled=white_label_enabled,
            viewer_3_d_enabled=viewer_3_d_enabled,
            adapters_enabled=adapters_enabled,
            white_label_css=white_label_css,
            demo_mode_enabled=demo_mode_enabled,
            teleop_share_enabled=teleop_share_enabled,
            bill_estimate_enabled=bill_estimate_enabled,
            data_retention_enabled=data_retention_enabled,
            days_data_retained=days_data_retained,
            max_chunk_request_limit=max_chunk_request_limit,
            support_enabled=support_enabled,
            support_tier=support_tier,
            trial_period_end=trial_period_end,
            external_id=external_id,
            chargebee_id=chargebee_id,
            totango_id=totango_id,
            custom_tos=custom_tos,
            teleop_enabled=teleop_enabled,
            observability_enabled=observability_enabled,
            share_enabled=share_enabled,
            annotations_enabled=annotations_enabled,
            diagnostics_enabled=diagnostics_enabled,
            ssh_enabled=ssh_enabled,
            spot_enabled=spot_enabled,
            file_storage_enabled=file_storage_enabled,
            role_viewer_enabled=role_viewer_enabled,
            teams_enabled=teams_enabled,
            schedules_enabled=schedules_enabled,
            paging_enabled=paging_enabled,
            stateful_events_enabled=stateful_events_enabled,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        organization.additional_properties = d
        return organization

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
