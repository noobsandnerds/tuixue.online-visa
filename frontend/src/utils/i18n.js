import i18n from "i18next";
import countries from "i18n-iso-countries";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

// register languages for browser versions
countries.registerLocale(require("i18n-iso-countries/langs/en.json"));
countries.registerLocale(require("i18n-iso-countries/langs/zh.json"));

export { countries };

const resources = {
    en: {
        translation: {
            countryCode: "{{countryName, country}}",
            visaStatus: "Visa Status",
            webNotify: "Auto Web Notify",
            sysStatus: "System Status",
            checkee: "Check Reporter",
            filterDesc: "Choose Embassy/Consulate",
            filterSystemDesc: "Filter by system: ",
            filterDefault: "Reset to default",
            filterDomestic: "Domestic only",
            filterOverviewOpen: "Show Charts",
            filterOverviewClose: "Collapse Charts",
            overMinuteChartTitle: "First available appointment change within 24h",
            overDateChartTitle: "Appointment change within 60 days - {{embassyName}}",
            at: "at",
            all: "All",
            refreshDone: "Done with refresh",
            overviewTitle: "Visa Status Overview",
            overviewEarliest: "Earliest availabe appointment date of today",
            overviewNewest: "Latest fetching result of available appointment date",
            overviewLatest: "Latest available appointment date of today",
            overviewEmailIcon: "Subscribe from email",
            overviewQQIcon: "Subscribe from QQ group / Telegram channel",
            overviewAddtionalIcon: "Additional information",
            overviewEarliestDate: "Earliest Date",
            overviewLatestDate: "Latest Date",
            overviewNewestFetch: "Newest Fetch",
            overviewActions: "Actions",
            notificationInitTitle: "Auto-notification is enabled",
            notificationInitContent: "If a new position pops up, the browser will pop up a notification ASAP",
            notificationTitle: "{{visaTypeDetail}} Visa Status Changed",
            notificationContent: "{{embassyName}} changed from {{prevAvaiDate}} to {{currAvaiDate}}.",
            notificationBlocked: "Notifications blocked. Please enable it in your browser.",
            notificationNoSupport: "This browser does not support web notification.",
            QQTGModalTitle: "QQ Group and Telegram Channel Subscription for F1 Visa",
            TGDomestic: "Telegram Channel link (domestic): ",
            TGNonDomestic: "Telegram Channel link (global): ",
            QQDescDomestic:
                "QQ group entry password is the site URL, a total of 13 characters t***e. All groups' content are the same.",
            QQDescNonDomestic:
                "The global version includes popular areas for getting visa in third country, including {{cities}}",
            QQGroupDomestic: "Domestic #{{index}}: ",
            QQGroupNonDomestic: "Global #{{index}}: ",
            counterFooterP1: "This website has witnessed a total of ",
            counterFooterP2: " tuixue (withdrawals).",
            disqusDomestic: "Disqus (Domestic version)",
            disqusGlobal: "Disqus (Global version)",
            disqusLoadFail: "Unable to load Disqus comments :(",
        },
    },
    zh: {
        translation: {
            countryCode: "{{countryName, country}}",
            visaStatus: "签证预约状态",
            webNotify: "网页自动通知",
            sysStatus: "系统当前状态",
            checkee: "签证结果统计",
            filterDesc: "选择使领馆",
            filterSystemDesc: "选择系统：",
            filterDefault: "恢复默认",
            filterDomestic: "只看国内",
            filterOverviewOpen: "展开图表",
            filterOverviewClose: "收起图表",
            overMinuteChartTitle: "24h内可预约日期变动情况",
            overDateChartTitle: "{{embassyName}}60天内预约日期变动情况",
            at: "于",
            all: "全部",
            Refresh: "刷新数据",
            refreshDone: "已刷新至最新数据",
            Location: "地点",
            overviewTitle: "美国签证预约时间",
            overviewEarliest: "今天出现的最早可预约日期",
            overviewNewest: "当前日期",
            overviewLatest: "今天出现的最晚可预约日期",
            overviewEmailIcon: "邮件订阅",
            overviewQQIcon: "QQ群/Telegram频道订阅",
            overviewAddtionalIcon: "更多信息",
            overviewEarliestDate: "最早日期",
            overviewLatestDate: "最晚日期",
            overviewNewestFetch: "当前日期",
            overviewActions: "操作",
            notificationInitTitle: "已开启自动通知功能",
            notificationInitContent: "如果有新位置放出来，浏览器会第一时间弹出通知",
            notificationTitle: "{{visaTypeDetail}} 签证放新位置了",
            notificationContent: "{{embassyName}}: {{prevAvaiDate}} -> {{currAvaiDate}}",
            notificationBlocked: "通知被浏览器屏蔽了，请手动打开它",
            notificationNoSupport: "这个浏览器不支持网页版通知",
            TGDomestic: "Telegram 频道（国内版）链接：",
            TGNonDomestic: "Telegram 频道（国际版）链接：",
            QQDescDomestic: "QQ群入群密码是本站网址，共13个字符t***e，所有群内容一致",
            QQDescNonDomestic: "国际版仅包含目前第三国签证热门地区，包括：{{cities}}",
            QQTGModalContentQQ: "QQ群{{index}}群：",
            QQGroupDomestic: "国内{{index}}群：",
            QQGroupNonDomestic: "国际{{index}}群：",
            counterFooterP1: "本网站一共见证了",
            counterFooterP2: "人次的失学。",
            disqusDomestic: "原国内版评论区",
            disqusGlobal: "原国际版评论区",
            disqusLoadFail: "Disqus评论区无法加载 :(",
        },
    },
};

i18n.use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources,
        fallbacklng: "zh",
        interpolation: {
            escapeValue: false,
            format: (value, format, lng) =>
                format === "country" ? countries.getName(value, lng, { select: "official" }) : value,
        },
    });

export const namespace = "translation";
export const lngs = { en: "en", zh: "zh" };
export default i18n;
