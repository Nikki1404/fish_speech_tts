py -3.11 prepare_chunks_local.py --csv data/inspira_transcripts.csv --wav-dir raw_wavs --out-dir loadtest_chunks --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --chunk-sec 10 --language en-US

notepad loadtest_chunks\REVIEW_LOW_SCORE.txt

py -3.11 load_test_until_failure.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure

py -3.11 load_test_until_failure.py --mode ws --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure


(venv) PS C:\Users\re_nikitav\Documents\nemotron_finetuned> pip install -r requirements_load_test
Fatal error in launcher: Unable to create process using '"C:\Users\re_nikitav\Desktop\bu-digital-cx-speech-asr-realtime-custom-vad\scripts\venv\Scripts\python.exe"  "C:\Users\re_nikitav\Desktop\asr\bu-digital-cx-speech-asr-realtime-custom-vad\scripts\venv\Scripts\pip.exe" install -r requirements_load_test': The system cannot find the file specified.


python load_test_autoscaling.py --mode ws --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 1 --step 5 --max-concurrency 60 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled

python load_test_autoscaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 37 --step 1 --max-concurrency 41 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled

  python load_test_autoscaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1" --start-concurrency 1 --step 5 --max-concurrency 60 --stage-seconds 90 --metrics-delay 135 --rest-seconds 10 --stop-when-scaled
py -3.11 load_test_until_failure_with_scaling.py --mode http --manifest loadtest_chunks\manifest.jsonl --base-url "https://nemotron-3-5-150916788856.us-central1.run.app" --until-failure --start-concurrency 1 --step 1 --max-concurrency 50 --rounds 1 --rest 5 --confirm-failure --monitor-scaling --project-id "emr-dgt-autonomous-uctr1-snbx" --service-name "nemotron-3-5" --region "us-central1"


ing fee applies
----------------------------------------------------------------------------------------------------
[CONFIRM RESULT] 43/50 successful

##########################################################################################
AUTO-RAMP RESULT (HTTP)
Last fully successful concurrency : 43
First failing concurrency         : 50
##########################################################################################

Saved JSON: nemotron_loadtest_20260810_131107.json
Saved CSV : nemotron_loadtest_20260810_131107.csv

====================================================================================================
CLOUD RUN AUTOSCALING CHECK
====================================================================================================
Waiting 130s once for Cloud Monitoring instance-count data...

Instance-count samples:
  2026-08-10T07:23:00+00:00 | instances=1 | mapped_concurrency=None (before)
  2026-08-10T07:24:00+00:00 | instances=1 | mapped_concurrency=15 (during)
  2026-08-10T07:25:00+00:00 | instances=1 | mapped_concurrency=15 (after)
  2026-08-10T07:26:00+00:00 | instances=1 | mapped_concurrency=22 (during)
  2026-08-10T07:27:00+00:00 | instances=1 | mapped_concurrency=29 (during)
  2026-08-10T07:28:00+00:00 | instances=1 | mapped_concurrency=29 (during)
  2026-08-10T07:29:00+00:00 | instances=1 | mapped_concurrency=36 (during)
  2026-08-10T07:30:00+00:00 | instances=1 | mapped_concurrency=36 (during)
  2026-08-10T07:31:00+00:00 | instances=1 | mapped_concurrency=36 (during)
  2026-08-10T07:32:00+00:00 | instances=1 | mapped_concurrency=43 (during)
  2026-08-10T07:33:00+00:00 | instances=1 | mapped_concurrency=43 (during)
  2026-08-10T07:34:00+00:00 | instances=1 | mapped_concurrency=43 (during)
  2026-08-10T07:35:00+00:00 | instances=1 | mapped_concurrency=50 (during)
  2026-08-10T07:36:00+00:00 | instances=1 | mapped_concurrency=50 (during)
  2026-08-10T07:37:00+00:00 | instances=1 | mapped_concurrency=50 (during)

----------------------------------------------------------------------------------------------------
RESULT: No second Cloud Run instance was observed during the tested concurrency range.
----------------------------------------------------------------------------------------------------
Note: Cloud Monitoring instance_count is sampled periodically, so this is the first observed concurrency associated with pod 2, not a millisecond-exact autoscaler trigger.
====================================================================================================
(venv) PS C:\Users\re_nikitav\Documents\nemotron_finetuned>
