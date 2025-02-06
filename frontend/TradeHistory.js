import React, { useState, useEffect } from "react";

const TradeHistory = () => {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        const fetchTradeHistory = async () => {
            try {
                const response = await fetch("/api/trade-history"); // Ensure your backend serves this endpoint
                const data = await response.json();
                setTrades(data);
            } catch (error) {
                console.error("Error fetching trade history:", error);
            }
        };

        fetchTradeHistory();
    }, []);

    return (
        <div className="p-6 bg-gray-900 text-white rounded-lg shadow-md">
            <h2 className="text-xl font-bold mb-4">Trade History</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-gray-800 text-white border border-gray-700">
                    <thead>
                        <tr className="border-b border-gray-700">
                            <th className="px-4 py-2">Timestamp</th>
                            <th className="px-4 py-2">Token Pair</th>
                            <th className="px-4 py-2">Amount</th>
                            <th className="px-4 py-2">Profit (ETH)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades.length > 0 ? (
                            trades.map((trade, index) => (
                                <tr key={index} className="border-b border-gray-700">
                                    <td className="px-4 py-2">
                                        {new Date(trade.timestamp * 1000).toLocaleString()}
                                    </td>
                                    <td className="px-4 py-2">{trade.tokenPair}</td>
                                    <td className="px-4 py-2">{trade.amount}</td>
                                    <td className="px-4 py-2 text-green-400">{trade.profit} ETH</td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan="4" className="text-center px-4 py-2">
                                    No trade history available
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TradeHistory;