import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { ethers } from "ethers";

const Dashboard = () => {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        async function fetchTrades() {
            try {
                // Simulating an API call to fetch latest trades
                const response = await fetch("/api/trades");
                const data = await response.json();
                setTrades(data);
            } catch (error) {
                console.error("Error fetching trades:", error);
            }
        }
        fetchTrades();
    }, []);

    return (
        <Card className="p-4">
            <CardContent>
                <h2 className="text-xl font-bold mb-4">Live Arbitrage Trades</h2>
                <ul>
                    {trades.length > 0 ? (
                        trades.map((trade, index) => (
                            <li key={index} className="mb-2">
                                <strong>Token Pair:</strong> {trade.tokenPair} <br />
                                <strong>Profit:</strong> {ethers.formatEther(trade.profit)} ETH
                            </li>
                        ))
                    ) : (
                        <p>No trades available</p>
                    )}
                </ul>
            </CardContent>
        </Card>
    );
};

export default Dashboard;