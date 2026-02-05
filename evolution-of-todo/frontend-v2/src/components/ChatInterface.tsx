import { useState, useEffect, useRef } from "react";
import { useSession } from "@/lib/auth-client";
import { apiRequest } from "@/lib/api";
import { Send, Bot, User, Loader2, PlayCircle } from "lucide-react";

interface ToolCall {
    name: string;
    args: any;
    result: any;
}

interface Message {
    role: "user" | "assistant";
    content: string;
    tool_calls?: ToolCall[];
}

export default function ChatInterface() {
    const { data: session } = useSession();
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !session?.user?.id) return;

        const userMsg = input;
        setInput("");
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setLoading(true);

        try {
            const res = await apiRequest(`/api/${session.user.id}/chat`, {
                method: "POST",
                body: JSON.stringify({
                    message: userMsg,
                    conversation_id: conversationId
                })
            });

            if (res.conversation_id) setConversationId(res.conversation_id);

            setMessages(prev => [...prev, {
                role: "assistant",
                content: res.response,
                tool_calls: res.tool_calls
            }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: "assistant", content: "Error: Failed to process request." }]);
        } finally {
            setLoading(false);
        }
    };

    if (!session) {
        return <div className="p-4 text-center">Please sign in to access the chat.</div>;
    }

    return (
        <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto border rounded-xl bg-white shadow-lg overflow-hidden font-sans">
            <div className="bg-gray-50 border-b p-4 flex items-center justify-between">
                <h2 className="font-semibold text-gray-700 flex items-center gap-2">
                    <Bot className="text-blue-600" /> Todo Agent
                </h2>
                <span className="text-xs text-gray-400">Powered by OpenAI & MCP</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-gray-50/50">
                {messages.length === 0 && (
                    <div className="text-center text-gray-400 mt-20 flex flex-col items-center">
                        <Bot size={48} className="mb-4 opacity-20" />
                        <p>Start a conversation to manage your tasks.</p>
                        <p className="text-sm">Try "Add buy milk" or "List my tasks"</p>
                    </div>
                )}
                {messages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[85%] rounded-2xl p-4 shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-sm' : 'bg-white text-gray-800 border border-gray-100 rounded-tl-sm'}`}>
                            <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
                            {msg.tool_calls && msg.tool_calls.length > 0 && (
                                <div className="mt-3 pt-3 border-t border-gray-100 text-xs space-y-2">
                                    <p className="font-medium opacity-70 flex items-center gap-1"><PlayCircle size={10} /> Actions Taken:</p>
                                    {msg.tool_calls.map((tc, idx) => (
                                        <div key={idx} className="bg-gray-50/50 p-2 rounded border border-gray-100/50 font-mono text-[10px] overflow-x-auto">
                                            <div className="text-blue-500 font-bold">{tc.name}</div>
                                            <div className="text-gray-500 truncate opacity-70">Args: {JSON.stringify(tc.args)}</div>
                                            <div className="text-green-600 truncate mt-1">Result: {typeof tc.result === 'string' ? tc.result : JSON.stringify(tc.result)}</div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white p-3 rounded-2xl rounded-tl-sm border border-gray-100 shadow-sm flex items-center gap-2 text-gray-500 text-sm">
                            <Loader2 className="animate-spin" size={16} />
                            Thinking...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="p-4 border-t bg-white">
                <div className="flex gap-2 relative">
                    <input
                        className="flex-1 border border-gray-200 bg-gray-50 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all shadow-sm"
                        placeholder="Type a command..."
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading || !input.trim()} className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors shadow-sm">
                        <Send size={20} />
                    </button>
                </div>
            </form>
        </div>
    );
}
