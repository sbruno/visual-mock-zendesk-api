

import assert from "assert";
import { getGlobalState } from "../persist.js";
import { getCurrentTimestamp, portNumber } from "./helpers.js";

export function getJobById(jobId) {
    const globalState = getGlobalState()
    const result = globalState['jobresults'][jobId]
    assert(result, 'job not found ' + jobId)
    return renderCompletedJob(jobId, result)
}

export function renderPendingJob(jobId) {
    return {
        job_status: {
            id: jobId,
            url: `http://localhost:${portNumber}/api/v2/job_statuses/${jobId}.json`,
            "status":"pending"
        }
    }
}

export function renderCompletedJob(jobId, payload) {
    return {
        job_status: {
            id: jobId,
            url: `http://localhost:${portNumber}/api/v2/job_statuses/${jobId}.json`,
            "status":"completed",
            message: `Completed at ${getCurrentTimestamp()}`,
            results: payload
        }
    }
}