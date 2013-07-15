curl -H "Content-type: application/json" -X POST http://127.0.0.1:4000/jobs/new -d '{"job_args":["http://aaaa/bbb", "xxxxsha1xxxx"], "return_url":"http://www.cloudbase.it/testpost", "results_email":"your@email.com", "auth_key":"your_secret_key_here", "job_name":"openstack_create_instance"}'

