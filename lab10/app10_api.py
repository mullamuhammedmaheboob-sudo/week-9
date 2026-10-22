
import streamlit as st
import requests

st.title("Weather API Demo")

API_KEY = st.secrets.get("API_KEY", "demo_key")

city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):

    
    with st.spinner("Fetching weather..."):

        
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

       
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            resp = r.json()

            st.json(resp)

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Temperature",
                f"{resp['main']['temp']} C"
            )

            c2.metric(
                "Condition",
                resp["weather"][0]["main"]
            )

            c3.metric(
                "Humidity",
                f"{resp['main']['humidity']}%"
            )

        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again.")

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status == 401:
                st.error(
                    "OpenWeather rejected the API key (401). Check API_KEY in "
                    ".streamlit/secrets.toml against your OpenWeather account. "
                    "If you just created the key, allow a couple of hours for activation."
                )
            else:
                st.error(f"Weather request failed (HTTP {status}). Try again later.")

        except requests.exceptions.RequestException:
            st.error("Could not connect to OpenWeather. Check your internet connection.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("---")

st.subheader("HTTP Methods")

st.markdown("""
- **GET** - Retrieve data
- **POST** - Send data
- **PUT** - Update data
- **DELETE** - Delete data
""")
