# visualfabriq
Setup for parsers that have successfully parsed through nested JSON file types used to send Sell-In, Sell-Thru,  and Sell-Out data to Visualfabriq Bifrost (Inbound messages), and Parsed through outbound messages containing financial information pertaining to promotional activity.

Visualfabriq (aka VF RGM) is a Revenue Growth Management tool that integrated with SAP, or a SAP driven data lake, and uses the data to drive a web-based Trade Promotions (TPM), and Revenue Forecast model. These tools are driven and supported by in platform Demand Planning, claims/settlement, and reporting modules. 
The challenges facing many integrations for VF, is that there is no way to reliably triage/analyse the inbound and outbound messages data, in a manner that can confidently identify flaws/gaps/errors in the data being sent from SAP/Datalake to VF Bifrost (Bifrost is the repository for VF). This is a common problem for users of Visualfabriq. 

The code snippets in this Github repository successfully setup for parsers that have successfully done the following for a major VF client (Nestlé): 

Parsed through nested JSON file types used to send Sell-In, Sell-Thru, 
and Sell-Out data to Visualfabriq Bifrost (Inbound messages)

Parsed through outbound messages containing financial information pertaining to
promotional activity.

These parsers were used to triage an issue with data in SAP vs. Visualfabriq
They could easily be adapted to setup monitoring 

The .py will need to be modified to meet each customers needs. In this particular instance, Nestlé was sending faulty information to VF but had no visibility to the errors, since the data in SAP was accurate; the issue was occuring in a middleware platform during the generation of JSON files (of which there were thousands sent daily). 

HOPE THIS HELPS SOMEONE OUT THERE
DOPPLERCOCKPIT
