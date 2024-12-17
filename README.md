# ba-aftaler

## Overview

This README provides the necessary information to set up, configure, and use the microservice. It includes details about environmental variables, API endpoints, and dependencies.

The service can be accesed here: https://ba-aftaler-asathva5fdfscgb5.northeurope-01.azurewebsites.net/apidocs


---

## Environmental Variables

The microservice requires the following environmental variables to be configured before running. Ensure these variables are set correctly in your environment.

| Variable  | Required | Default | Description                |
| --------- | -------- | ------- | -------------------------- |
| `DB_PATH` | Yes      | None    | Path to the database file. |
|`KUNDER_SERVICE_URL`|Yes|None|Path to the Kunder microservice.|
|`BILER_SERVICE_URL`|Yes|None|Path to the Biler microservice.|

---


| **Path**       | **Method** | **Description** | **Status Codes**  | **Response** |
|------------|------------|--------------------|---------------|---------------------|
| `/aftaler`     | GET        | Retrieves a list of all aftaler stored in the database. | 200, 404  | Array of objects each containing `aftale_id`, `cpr`, `nummerplade`, `aftale_type`, `start_dato` and `slut_dato` or error message explaining failure. |
| `/aftaler`     | POST       | Creates a new aftale in the database after validating data with external microservices. | 201, 400, 404, 409, 500  | Object containing `aftale_id`, `cpr`, `nummerplade`, `aftale_type`, `start_dato` and `slut_dato` or error message explaining failure. |

---

## Dependencies

The following dependencies are required to run the microservice. These are specified in the `requirements.txt` file.

---
