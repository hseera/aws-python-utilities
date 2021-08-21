var synthetics = require('Synthetics');
const log = require('SyntheticsLogger');
const syntheticsConfiguration = synthetics.getConfiguration();


const apiCanaryBlueprint = async function () {

    syntheticsConfiguration.setConfig({
        restrictedHeaders: [], // Value of these headers will be redacted from logs and reports
        restrictedUrlParameters: [] // Values of these url parameters will be redacted from logs and reports
    });
    
    // Handle validation for positive scenario
    const validateSuccessful = async function(res) {
        return new Promise((resolve, reject) => {
            if (res.statusCode < 200 || res.statusCode > 299) {
                throw res.statusCode + ' ' + res.statusMessage;
            }
     
            let responseBody = '';
            res.on('data', (d) => {
                responseBody += d;
            });
     
            res.on('end', () => {
                // Add validation on 'responseBody' here if required.
                resolve();
            });
        });
    };
    

    // Set request option for workload-api
    let requestOptionsStep1 = {
        hostname: 'xxxx',
        method: 'GET',
        path: 'xxxx',
        port: '443',
        protocol: 'https:',
        body: "",
        headers: {"x-api-key":"xxx"}
    };
    requestOptionsStep1['headers']['User-Agent'] = [synthetics.getCanaryUserAgentString(), requestOptionsStep1['headers']['User-Agent']].join(' ');

    // Set step config option for workload-api
   let stepConfig1 = {
        includeRequestHeaders: false,
        includeResponseHeaders: false,
        includeRequestBody: false,
        includeResponseBody: false,
        continueOnHttpStepFailure: true
    };

    await synthetics.executeHttpStep('workload-api', requestOptionsStep1, validateSuccessful, stepConfig1);

    
};

exports.handler = async () => {
    return await apiCanaryBlueprint();
};

