

import assert from "assert";
import { getGlobalState } from "../persist.js";
import { getCurrentTimestamp, getPortNumber } from "./helpers.js";

export function apiGetJobById(jobId) {
    const globalState = getGlobalState()
    const result = globalState?.['jobresults']?.[jobId]
    if (!result) {
        throw new Error(`job not found ${jobId}`)
    }
    return renderCompletedJob(jobId, result)
}

export function renderPendingJob(jobId) {
    const globalState = getGlobalState()
    return {
        job_status: {
            id: jobId,
            url: `http://localhost:${getPortNumber()}${globalState.globalConfigs.overrideJobStatusUrlPrefix}/api/v2/job_statuses/${jobId}.json`,
            "status": "queued",
            total: None,
            progress: None,
            message: None,
            results: None
        }
    }
}

export function renderCompletedJob(jobId, payload) {
    const globalState = getGlobalState()
    return {
        job_status: {
            id: jobId,
            url: `http://localhost:${getPortNumber()}${globalState.globalConfigs.overrideJobStatusUrlPrefix}/api/v2/job_statuses/${jobId}.json`,
            "status": "completed",
            total: payload?.length,
            progress: payload?.length,
            message: `Completed at ${getCurrentTimestamp()}`,
            results: payload
        }
    }
}
