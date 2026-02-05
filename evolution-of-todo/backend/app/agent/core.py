import json
import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from app.mcp.server import add_task, list_tasks, complete_task, delete_task, update_task

import requests
import json

API_KEY = os.environ.get("OPENAI_API_KEY")
# Ensure we use the latest key provided by the user if it's in env
if not API_KEY or API_KEY == "sk-placeholder-replace-me":
    API_KEY = "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"

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",
    "X-Title": "Evolution of Todo App",
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create/Add a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List/Show tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["completed", "pending"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete/Remove a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

TOOL_MAP = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task
}

def run_agent(user_id: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Run the agent with the given message history."""
    
    system_message = {
        "role": "system",
        "content": f"""You are an AI assistant for a Todo application.
Current User ID: {user_id}
1. Always infer intent before responding.
2. Never manipulate tasks directly; always call MCP tools.
3. If required parameters are missing, ask a clarifying question.
4. After every tool call, confirm the action in natural language.
5. On errors (e.g., task not found), respond politely and suggest next steps."""
    }
    
    # Prepare messages
    full_messages = [system_message] + messages
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "sk-placeholder-replace-me":
        return {
            "content": "I'm sorry, but my OpenAI API key is not configured. Please add a valid `OPENAI_API_KEY` to the `backend/.env` file to enable the chat feature.",
            "tool_calls": []
        }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": full_messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "max_tokens": 500
    }

    try:
        print(f"DEBUG: Sending request to OpenRouter with model='openai/gpt-4o-mini', max_tokens=500")
        response = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"DEBUG: OpenRouter Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        error_msg = str(e)
        if 'response' in locals() and hasattr(response, 'text'):
            error_msg = f"{e} - {response.text}"
        print(f"Error in OpenRouter request: {error_msg}")
        return {
            "content": f"Error communicating with AI: {error_msg}",
            "tool_calls": []
        }

    
    choice = data['choices'][0]['message']
    content = choice.get('content')
    tool_calls = choice.get('tool_calls')

    
    # Return response message and any tool calls to be processed by the caller or loop here?
    # Specification 8.6 says: "5. Run the OpenAI Agent with MCP tools. 6. Persist assistant response and tool call metadata."
    # So we should probably handle the loop or return the intermediate state?
    # Spec 2.1: "7. Agent generates a confirmation response. 8. Response, tool calls... returned."
    
    if tool_calls:
        # Execute tools
        full_messages.append({
            "role": "assistant",
            "content": content,
            "tool_calls": tool_calls
        })
        
        executed_tool_calls_info = []
        
        for tool_call in tool_calls:
            function_info = tool_call.get('function', {})
            function_name = function_info.get('name')
            function_args = json.loads(function_info.get('arguments', '{}'))
            
            tool_function = TOOL_MAP.get(function_name)
            if tool_function:
                tool_result = tool_function(**function_args)
                
                full_messages.append({
                    "tool_call_id": tool_call.get('id'),
                    "role": "tool",
                    "name": function_name,
                    "content": str(tool_result)
                })
                
                executed_tool_calls_info.append({
                    "name": function_name,
                    "args": function_args,
                    "result": tool_result
                })
        
        # Second turn to generate confirmation
        try:
            payload_final = {
                "model": "openai/gpt-4o-mini",
                "messages": full_messages,
                "max_tokens": 500
            }
            res_final = requests.post(BASE_URL, headers=HEADERS, json=payload_final, timeout=30)
            res_final.raise_for_status()
            data_final = res_final.json()
            return {
                "content": data_final['choices'][0]['message'].get('content'),
                "tool_calls": executed_tool_calls_info
            }
        except Exception as e:
            error_msg = str(e)
            if 'res_final' in locals() and hasattr(res_final, 'text'):
                error_msg = f"{e} - {res_final.text}"
            print(f"Error in second OpenRouter request: {error_msg}")
            return {
                "content": f"Action was taken but I couldn't generate a text response: {error_msg}",
                "tool_calls": executed_tool_calls_info
            }
    else:
        return {
            "content": content,
            "tool_calls": []
        }

