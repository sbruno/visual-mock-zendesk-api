

import assert from "assert";

export function get_job_result(globalState, queryParams) {
    const result = globalState['jobresults'][jobId]
    assert(result, 'job not found ' + jobId)
    return result
}

