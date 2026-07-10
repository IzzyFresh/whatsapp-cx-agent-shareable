from typing import Any, Optional
def fake_tool_call(tool: Tool, input: dict[str, Any], callback_context: CallbackContext) -> Optional[dict[str, Any]]:
    confirmation_code = input.get("confirmation_code", "").upper()
    
    # Mock database with your specific info
    tickets = {
        "ISR123": {
            "status": "Confirmed",
            "flight": "CM789",
            "origin": "San Jose, CA (SJC)",
            "destination": "Atlanta, GA (ATL)",
            "date": "2026-05-27",
            "departure_time": "12:00 PM",
            "passenger": "Israel Castillo",
            "boarding_pass_link": "https://example.com/bp/isr123"
        }
    }
    
    # Lookup the ticket or return your info as the fallback
    if confirmation_code in tickets:
        return {"result": tickets[confirmation_code]}
    else:
        return {
            "result": {
                "status": "Confirmed",
                "flight": "CM789",
                "origin": "San Jose, CA (SJC)",
                "destination": "Atlanta, GA (ATL)",
                "date": "2026-05-27",
                "departure_time": "12:00 PM",
                "passenger": "Israel Castillo",
                "boarding_pass_link": f"https://example.com/bp/{confirmation_code.lower() if confirmation_code else 'default'}"
            }
        }