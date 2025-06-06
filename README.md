# Lab #16 (Azure Version)

## DISCLAIMER: The Lab were written by CHATGPT, this is only giving the step-by-step with not photos.  Included is a link to a Google Doc showing a more indepth instruction with photos.  https://docs.google.com/document/d/1M1ti1J-qb45ZNuYtd-B7fetRdyHoEbDtt2zSXqWbCQE/edit?usp=sharing

## Serverless Computing – Azure Logic Apps with Gmail and Azure Functions

### Objective

Create an automated system using Microsoft Azure Logic Apps that sends a daily "Bad Visualization of the Day" email using a Gmail account. This lab replaces AWS Lambda and SNS with Azure Logic Apps and Gmail. Jokes will be stored and retrieved dynamically from Azure Cosmos DB using an Azure Function.

---

## Section 1: Prerequisites

### Required Tools:

* An active Azure account
* A Gmail account
* A visulaization (or several) for testing

### Optional:

* Visual Studio Code with Azure Functions extension
* Python or Node.js development environment

### Resource Group:
Make Sure you have an active resource group for the Lab.
   * Call is `intials-cs178-lab16-resource`

---

## Section 2: Create a Logic App

### Steps:

1. Go to the Azure Portal.
2. Search for **Logic Apps** in the search bar.
3. Click **Create**.
   * **Hosting Option**: Click on Multi-tenant.
5. Fill out the form:

   * **Subscription**: Your Azure subscription
   * **Resource group**: Create new or select existing
   * **Logic App name**: `SendVisLogicApp`
   * **Region**: East US
6. Click **Review + Create**, then **Create**.

---

## Section 3: Add Recurrence Trigger

1. Open the Logic App Designer.
2. Select the **Recurrence** trigger.
3. Configure it as:

   * **Interval**: `1`
   * **Frequency**: `Day`
4. Expand **Advanced options**:

   * Set **Time Zone** to `Central Time`.
   * Set **Start time** to `2025-05-15T00:00:00Z` to start sending the emails.
   * Set **At These Hours** to `7` for 7:00AM
5. Click Save

---

## Section 4: Create Azure Cosmos DB Table

1. Go to Azure Portal, search for **Cosmos DB**.
2. Click **Create**, and choose **NoSQL** API.
3. Enter the following information as seen below:
4. Once created, go to the **Data Explorer** section.
5. Create a new **Database** called `BadVisualizations`.
6. Within the database, create a **Container**:

   * **Container ID**: `Visualizations`
   * **Partition key**: `/uuid`
7. Insert documents manually using the Data Explorer:

Example documents:

```json
{
  "uuid": "1",
  "image": "Converted Image to base64"
}
```

Use: 

Base64 Converter: https://www.base64-image.de/

UUID Generator: https://www.uuidgenerator.net/version4

Add at least three visualizations with different UUIDs.

---

## Section 5: Create an Azure Function to Retrieve Random Visualization

### Option A: Using Azure Portal

1. Go to Azure Portal, search for **Function App**, click **Create**.
2. Choose the same resource group.
3. Function App name: `BadVisualizationFunctionApp`
4. Runtime stack: Python or Node.js
5. Plan type: Consumption
6. After creation, click on the Function App > Functions > Create Function.
7. Choose **HTTP trigger**, name it `GetRandomVis`, choose **Anonymous**.

### Option B: Using VS Code (Recommended for Development)

1. Install Azure Functions extension in VS Code.
2. Open a new folder, open terminal:

   ```bash
   func init BadVisualizationFunctionApp --python
   cd BadVisulazationFunctionApp
   func new --name GetRandomVis --template "HTTP trigger"
   ```
3. Replace `function_app.py` content with `lab16-function_app.py`

4. Add `COSMOS_ENDPOINT` and `COSMOS_KEY` as environment variables in your Azure Function configuration.
5. Deploy to Azure using VS Code Azure extension.

---

## Section 6: Update Logic App to Use Azure Function

1. In Logic App Designer, click **+ New Step** after the recurrence trigger.
2. Search for **Azure Function**.
3. Choose your Function App and select the `GetRandomVis` function.
4. No additional parameters are required.
5. Add another **step**, search for **Gmail**, choose **Send Email (V2)**.
6. Configure Gmail:

   * **To**: `sophie.meronek@drake.edu@gmail.com`
   * **Subject**: `Bad Visualization`
   * **Body**: Click in the body field and insert the joke from the Azure Function's response (use dynamic content).

---

## Section 7: Test the Logic App

1. In the Logic App Designer, click **Run Trigger**.
2. Go to your Gmail inbox.
3. Confirm that the email with a joke was received.

---

## Section 8: Final Steps

* Confirm schedule is set for 7:00 AM daily.
* Confirm email is reaching intended recipient(s).
* Optionally, add more jokes or use a more advanced query to personalize jokes.

---

## Submission Instructions

1. Take a screenshot of your Logic App Designer and Azure Function code.
2. Trigger the workflow manually.
3. Submit the screenshot to your course portal.
4. Ensure Sophie receives an email with your visualization.

---

## Additional Resources

* [Azure Logic Apps Documentation](https://learn.microsoft.com/en-us/azure/logic-apps/)
* [Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)
* [Gmail Connector for Logic Apps](https://learn.microsoft.com/en-us/connectors/gmail/)
* [Azure Cosmos DB Documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/)

---
