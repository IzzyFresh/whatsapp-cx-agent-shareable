from typing import Any, Optional

def fake_tool_call(tool: Tool, input: dict[str, Any], callback_context: CallbackContext) -> Optional[dict[str, Any]]:
    # Check which tool is being called
    tool_name = getattr(tool, 'name', '')
    
    # Handler for query_ticket
    if tool_name == "query_ticket" or ("confirmation_code" in input and "bag_count" not in input):
        confirmation_code = input.get("confirmation_code", "").upper()
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
        
    # Handler for add_checked_bag
    elif tool_name == "add_checked_bag" or "bag_count" in input:
        confirmation_code = input.get("confirmation_code", "").upper()
        bag_count = int(input.get("bag_count", 1))
        
        fee_per_bag = 30
        total_fee = bag_count * fee_per_bag
        
        return {
            "result": {
                "status": "Success",
                "confirmation_code": confirmation_code,
                "bags_added": bag_count,
                "fee_amount": total_fee,
                "currency": "USD",
                "message": f"Successfully added {bag_count} bag(s) for ticket {confirmation_code}. A fee of ${total_fee} has been applied."
            }
        }
        
    return {"result": "mock result"}
