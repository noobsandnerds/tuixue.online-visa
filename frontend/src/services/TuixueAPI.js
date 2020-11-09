import * as tp from "./typeCheck";

const { REACT_APP_API_BASE_URL: API_BASE_URL } = process.env;
const metadata = "/visastatus/meta";
const overview = "/visastatus/overview";
const latest = "/visastatus/latest";
const singleStatus = (visaType, embassyCode) => `/visastatus/${visaType}/${embassyCode}`;

const HEADERS = {
    Accept: "application/json",
};

/**
 * Construct a REST api URL with given path and query parameters.
 * @param {string} path     REST api endpoint
 * @param {Object} query    Object used to construct query parameters
 * @return {string}         The constructed URL string
 */
const constructURL = (path, query = null) => {
    const url = new URL(path, API_BASE_URL);
    if (query) {
        for (const [paramKey, paramVal] of Object.entries(query)) {
            if (Array.isArray(paramVal)) {
                paramVal.forEach(val => url.searchParams.append(paramKey, val));
            } else {
                url.searchParams.append(paramKey, paramVal);
            }
        }
    }
    return url.toString();
};

/**
 * GET `${API_BASE_URL}/visastatus/meta`
 *
 * Get metadata on embassy/consulate categorization and embassy/consulate attributes.
 * @return {Object} The object containing metadata info.
 */
export const getVisaStatusMetadata = async () => {
    const url = constructURL(metadata);

    let res;
    let responseJson;
    try {
        res = await fetch(url, { method: "GET", headers: HEADERS });
        if (res.ok) {
            responseJson = await res.json();
        }
    } catch (e) {
        console.error(`In getVisaStatusMetadata: ${e}`);
    }

    return responseJson || null;
};

/**
 * GET `${API_BASE_URL}/visastatus/overview`
 *
 * Get visa status' `{earliest_date, latest_date}` of a givenv `date`
 * @param {Array|string} visaType Array of string standing for types of Visa.
 * @param {Array|string} embassyCode Array of string standing for a unqiue U.S. Embassy/Consulate.
 * @param {Date} since Datetime that stands for the start date of retrieving data.
 * @param {Date} to Datetime that stands for the end date of retrieving data.
 * @return {Array} An array of overviews aggregated by date.
 */
export const getVisaStatusOverview = async (visaType, embassyCode, since, to) => {
    if (!visaType || !embassyCode) {
        throw new Error(`visaTypes: ${visaType} or embassyCodes ${embassyCode} are not valid.`);
    }

    const visaTypeLst = Array.isArray(visaType) ? visaType : [visaType];
    const embassyCodeLst = Array.isArray(embassyCode) ? embassyCode : [embassyCode];
    if (!tp.checkVisaTypeLst(visaTypeLst)) {
        throw new Error(`In getVisaStatusOverview: received invalid visaType: ${visaType}`);
    }
    if (!tp.checkEmbassyCodeLst(embassyCodeLst)) {
        throw new Error(`In getVisaStatusOverview: received invalid embassyCode: ${embassyCode}`);
    }
    if (since && !tp.checkDateObj(since)) {
        throw new Error(`In getVisaStatusOverview: received invalid since: ${since}`);
    }
    if (to && !tp.checkDateObj(to)) {
        throw new Error(`In getVisaStatusOverview: received invalid to: ${to}`);
    }

    const queryParam = { visa_type: visaTypeLst, embassy_code: embassyCodeLst };
    if (since) {
        queryParam.since = since.toISOString().slice(0, -1);
    }
    if (to) {
        queryParam.to = to.toISOString().slice(0, -1);
    }

    const url = constructURL(overview, queryParam);

    let res;
    let responseJson;
    try {
        res = await fetch(url, { method: "GET", headers: HEADERS });
        if (res.ok) {
            responseJson = await res.json();
        }
    } catch (e) {
        console.error(`In getVisaStatusOverview: ${e}`);
    }

    return responseJson || null;
};

/**
 * GET `${API_BASE_URL}/visastatus/latest`
 *
 * Get the latest fetched result of `[visaType] x [embassyCode]`
 * @param {Array|string} visaType Array of string standing for types of Visa.
 * @param {Array|string} embassyCode Array of string standing for a unqiue U.S. Embassy/Consulate.
 */
export const getLatestVisaStatus = async (visaType, embassyCode) => {
    if (!visaType || !embassyCode) {
        throw new Error(`visaTypes: ${visaType} or embassyCodes ${embassyCode} are not valid.`);
    }

    const visaTypeLst = Array.isArray(visaType) ? visaType : [visaType];
    const embassyCodeLst = Array.isArray(embassyCode) ? embassyCode : [embassyCode];
    if (!tp.checkVisaTypeLst(visaTypeLst)) {
        throw new Error(`In getVisaStatusOverview: received invalid visaType: ${visaType}`);
    }
    if (!tp.checkEmbassyCodeLst(embassyCodeLst)) {
        throw new Error(`In getVisaStatusOverview: received invalid embassyCode: ${embassyCode}`);
    }

    const url = constructURL(latest, { visa_type: visaType, embassy_code: embassyCode });

    let res;
    let responseJson;
    try {
        res = await fetch(url, { method: "GET", headers: HEADERS });
        if (res.ok) {
            responseJson = await res.json();
        }
    } catch (e) {
        console.error(`In getLatestVisaStatus: ${e}`);
    }

    return responseJson || null;
};

/**
 * GET `${API_BASE_URL}/visastatus/${visaType}/${embassyCode}`
 *
 * Get the full fetched records of a `(visaType, embassyCode)` pair.
 * @param {string} visaType A single visaType string
 * @param {string} embassyCode A single embassyCode string
 * @param {Date} writeDate Date of the records for a `(visaType, embassyCode)` group
 * @return {Object} An object with shape of `{visa_type, embassy_code, write_date, available_dates}`
 */
export const getSingleVisaStatus = async (visaType, embassyCode, writeDate) => {
    if (!tp.checkVisaType(visaType)) {
        throw new Error(`In getSingleVisaStatus: received invalid visaType: ${visaType}`);
    }
    if (!tp.checkEmbassyCode(embassyCode)) {
        throw new Error(`In getSingleVisaStatus: received invalid embassyCode: ${embassyCode}`);
    }
    if (!tp.checkDateObj(writeDate)) {
        throw new Error(`In getSingleVisaStatus: received invalid writeDate: ${writeDate}`);
    }

    const path = singleStatus(visaType, embassyCode);
    const url = constructURL(path, { write_date: writeDate.toISOString().slice(0, -1) });

    let res;
    let responseJson;
    try {
        res = await fetch(url, { method: "GET", headers: HEADERS });
        responseJson = await res.json();
    } catch (e) {
        console.error(`In getSingleVisaStatus: ${e}`);
    }

    return responseJson || null;
};
