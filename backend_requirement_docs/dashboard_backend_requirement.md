Dashboard Page Backend Requirement Document

1\. Feature Overview

The Dashboard page should display real-time UV information based on the user's location and dynamically update the page content according to the UV level.

System flow:

User opens Dashboard

↓

Frontend detects location via IP

↓

Frontend sends location to backend

↓

Backend retrieves UV data

↓

Backend returns UV + dynamic content

↓

Frontend renders dashboard



2\. Frontend Responsibility

The frontend is responsible for:

1\. Detect the user's location via IP lookup

2\. Obtain location info such as:

Melbourne, Australia

3\. Send the location to the backend API

Example request:

POST /api/uv-dashboard

Request body(JSON):

{

&nbsp; "location": "Melbourne, Australia"

}

3\. Backend Responsibility

The backend is responsible for:

1\. Retrieve UV data based on the location

2\. Determine the UV risk level

3\. Generate dynamic dashboard content:

\- warning message



\- protection advice cards



\- Today's UV Summary



\- Quick Tips



4\. Return a complete JSON response for frontend rendering.

4\. Backend Response Structure

Recommended response structure (JSON):

TIPS: This is provided for illustrative purposes only.

{

&nbsp; "location": "Melbourne, Australia",

&nbsp; "uv\_index": 8,

&nbsp; "risk\_level": "Very High",

&nbsp; "warning\_message": "High UV – skin damage may occur quickly. Minimise sun exposure from 10 AM to 4 PM.",



&nbsp; "protection\_advice": \[

&nbsp;   {

&nbsp;     "title": "Apply Sunscreen",

&nbsp;     "description": "SPF 30+ every 2 hours"

&nbsp;   },

&nbsp;   {

&nbsp;     "title": "Wear Sunglasses",

&nbsp;     "description": "UV protective lenses"

&nbsp;   },

&nbsp;   {

&nbsp;     "title": "Wear a Hat",

&nbsp;     "description": "Wide-brimmed hat preferred"

&nbsp;   },

&nbsp;   {

&nbsp;     "title": "Seek Shade",

&nbsp;     "description": "Stay indoors during peak UV hours"

&nbsp;   }

&nbsp; ],



&nbsp; "uv\_summary": {

&nbsp;   "description": "UV levels are high today in Melbourne. Outdoor protection is strongly recommended.",

&nbsp;   "points": \[

&nbsp;     "Peak UV hours: 10 AM – 4 PM",

&nbsp;     "Recommended SPF: 30+",

&nbsp;     "Reapply sunscreen every 2 hours"

&nbsp;   ]

&nbsp; },



&nbsp; "quick\_tips": \[

&nbsp;   "Check UV before leaving home",

&nbsp;   "Carry sunscreen in your bag",

&nbsp;   "Choose shaded outdoor areas"

&nbsp; ]

}



5\. UV Level Mapping Rules

Backend should follow standard UV index classification.

|UV Index|Level|
|-|-|
|0–2|Low|
|3–5|Moderate|
|6–8	|High|
|8–10|Extreme|



6. Content Simulation for Each UV Level

Below are sample responses for each UV level.

UV Level 0–2 (Low)

1.Warning Message

Low UV – minimal protection required.

2.Protection Advice (1 card)

1\) Wear Sunglasses

UV protective lenses.

3.Today's UV Summary

UV levels are low today.

• Most people can safely stay outdoors.

• Sunglasses are recommended.

• Sunscreen optional for short exposure.

4.Quick Tips

• Check UV before outdoor plans

• Wear sunglasses on bright days

UV Level 3–5 (Moderate)

1.Warning Message

Moderate UV – protection recommended during midday.

2.Protection Advice (3 cards)

1\) Apply Sunscreen

SPF 30+ every 2 hours.

2\) Wear Sunglasses

UV protective lenses.

3\) Wear a Hat

Wide-brimmed hat preferred.

3.Today's UV Summary

UV levels are moderate today.

• Protection recommended around midday

• SPF 30+ recommended every 2 hours.

• Hats and sunglasses help reduce exposure

4.Quick Tips

• Apply sunscreen before leaving home

• Avoid long exposure at midday

• Bring sunglasses outdoors

UV Level 6–9 (High)

1.Warning Message

High UV – skin damage may occur quickly.

Minimise sun exposure from 10 AM to 4 PM.

2.Protection Advice (4 cards)

1\) Apply Sunscreen

SPF 30+ every 2 hours.

2\) Wear Sunglasses

UV protective lenses.

3\) Wear a Hat

Wide-brimmed hat recommended.

3.Today's UV Summary

UV levels are high today.

• Peak UV hours: 10 AM – 4 PM

• SPF 30+ recommended

• Reapply sunscreen every 2 hours

4.Quick Tips

• Carry sunscreen in your bag

• Choose shaded areas

• Check UV before outdoor activities

UV Level 9-11+ (Extreme)

1.Warning Message

Very High UV – unprotected skin can burn quickly.

Avoid outdoor exposure during peak hours.

2.Protection Advice (5 cards)

1)Apply Sunscreen

SPF 50+ every 2 hours.

2\) Wear Sunglasses

UV protective lenses.

3\) Wear a Hat

Wide-brimmed hat recommended.

4\) Seek Shade

Stay indoors during peak UV hours.

3.Today's UV Summary

UV levels are very high today.

• Peak UV hours: 10 AM – 4 PM.

• SPF 50+ recommended every 2 hours.

• Protective clothing strongly advised.

4.Quick Tips

• Limit outdoor activity

• Reapply sunscreen frequently

• Wear protective clothing

7\. Frontend Rendering Rules

Frontend should render UI based on backend response.

|UI Component	<br />&nbsp;					|Data Source|
|-|-|
|UV circle|uv\_index|
|Warning message|warning\_message|
|Advice cards|protection\_advice|
|Today's UV Summary|uv\_summary|
|Quick Tips|quick\_tips|



The frontend should not hardcode UV logic.

Please note that the frontend currently lacks functionality to retrieve the user's IP address for location data. Both the displayed location and unique visitor (UV) values are mocked. recommend implementing:

location = data\["location"]

uv\_index = data\["uv\_index"]

risk\_level = data\["risk\_level"]

warning\_message = data\["warning\_message"]

advice\_cards = data\["protection\_advice"]

uv\_summary = data\["uv\_summary"]

quick\_tips = data\["quick\_tips"]

8\. Future Scalability

Recommended additional fields:

uv\_color

risk\_icon

recommended\_spf

peak\_hours



For subsequent UI optimisation

