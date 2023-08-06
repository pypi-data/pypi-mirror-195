import requests

class SeekScraper:

    @classmethod
    def get_questions_answers(self, job_id: int):
        header = {
            'accept': 'application/features.seek.all+json, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.seek.com.au',
            'referer': f'https://www.seek.com.au/job/{job_id}/apply',
            'sec-ch-ua': '"Not A(Brand";v="24", "Chromium";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Linux',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'seek-request-brand': 'seek',
            'seek-request-country': 'AU',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-seek-ec-sessionid': '19827242-bdd8-4ec9-ad78-1e762e68402f',
            'x-seek-ec-visitorid': '19827242-bdd8-4ec9-ad78-1e762e68402f',
            'x-seek-site': 'ca-jobapply-frontend',
            'content-length': '4954'
        }
        data = [
            {
                'operationName': 'GetJobApplicationProcess',
                'variables': {
                    'jobId': f'{job_id}',
                    'isAuthenticated': True
                },
                'query': 'query GetJobApplicationProcess($jobId: ID!, $isAuthenticated: Boolean!) {\n  jobApplicationProcess(jobId: $jobId) {\n    ...location\n    ...classification\n    ...documents\n    ...questionnaire\n    job {\n      ...job\n      __typename\n    }\n    linkOut\n    extractedRoleTitles\n    __typename\n  }\n}\n\nfragment job on Job {\n  id\n  createdAt {\n    shortLabel\n    __typename\n  }\n  content\n  title\n  advertiser {\n    id\n    name\n    __typename\n  }\n  abstract\n  source\n  product {\n    id\n    ... on BrandedJobAd {\n      branding {\n        logo {\n          jdpLogo\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on PremiumJobAd {\n      branding {\n        logo {\n          jdpLogo\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment location on JobApplicationProcess {\n  location {\n    id\n    name\n    __typename\n  }\n  state {\n    id\n    __typename\n  }\n  area {\n    id\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment classification on JobApplicationProcess {\n  classification {\n    id\n    name\n    subClassification {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment documents on JobApplicationProcess {\n  documents {\n    lastAppliedResumeIdPrefill @include(if: $isAuthenticated)\n    selectionCriteriaRequired\n    lastWrittenCoverLetter @include(if: $isAuthenticated) {\n      content\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment questionnaire on JobApplicationProcess {\n  questionnaire {\n    questions @include(if: $isAuthenticated) {\n      id\n      text\n      __typename\n      ... on SingleChoiceQuestion {\n        lastAnswer {\n          id\n          text\n          __typename\n        }\n        options {\n          id\n          text\n          __typename\n        }\n        __typename\n      }\n      ... on MultipleChoiceQuestion {\n        lastAnswers {\n          id\n          text\n          __typename\n        }\n        options {\n          id\n          text\n          __typename\n        }\n        __typename\n      }\n      ... on PrivacyPolicyQuestion {\n        url\n        options {\n          id\n          text\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\n'
            }
        ]
        url = 'https://www.seek.com.au/graphql'
        resp = requests.post(url, json=data)
        data = resp.json()
        questions = data[0]['data']['jobApplicationProcess']['questionnaire']['questions']
        return {
            'job_url': f'https://www.seek.com.au/job/{job_id}',
            'questions': questions
        }