import React, { useState, useEffect } from "react";
import Dashboard from "./Dashboard";
import TradeHistory from "./components/TradeHistory";
import RiskSettings from "./components/RiskSettings";
import { Card } from "./components/ui/Card";
import { Button } from "./components/ui/Button";
import { ethers } from "ethers";

const App = () => {
    const [account, setAccount] = useState(null);

    useEffect(() => {
        async function loadWeb3() {
            if (window.ethereum) {
                const provider = new ethers.BrowserProvider(window.ethereum);
                const signer = await provider.getSigner();
                setAccount(await signer.getAddress());
            }
        }
        loadWeb3();
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Arbitrage Trading Dashboard</h1>
            <Card>
                <CardContent>
                    <p><strong>Connected Account:</strong> {account || "Not connected"}</p>
                    <Button onClick={() => window.ethereum.request({ method: 'eth_requestAccounts' })}>
                        Connect Wallet
                    </Button>
                </CardContent>
            </Card>
            <div className="grid grid-cols-3 gap-4 mt-6">
                <Dashboard />
                <TradeHistory />
                <RiskSettings />
            </div>
        </div>
    );
};

export default App;