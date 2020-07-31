DHI to Hydrotel
=================================================================

This git repository contains code necessary to transfer the DHI flood forecasting model output to Hydrotel.

The script runs on the dhi-mc01 VM (which is the same VM as the DHI models). The contents of this repo should be copied to the folder D:\scripts\dhi_to_hydrotel on dhi-mc01.

Run the install_env.bat as admin to install the appropriate python environment for the script to run in. Then import the dhi_to_hydrotel.xml into windows task scheduler and use svc-hydrotelexp-prod as the user to run the task.

The parameters.yml contains the parameters for the input and output. When more folders should be monitored, simply add them to the result_folders array.
