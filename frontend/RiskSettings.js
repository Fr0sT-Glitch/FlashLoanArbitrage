import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const RiskSettings = () => {
    const [slippageTolerance, setSlippageTolerance] = useState(0.005);
    const [maxGasPrice, setMaxGasPrice] = useState(100);
    
    useEffect(() => {
        async function fetchSettings() {
            try {
                const response = await fetch("/api/risk-settings");
                const data = await response.json();
                setSlippageTolerance(data.slippageTolerance);
                setMaxGasPrice(data.maxGasPrice);
            } catch (error) {
                console.error("Error fetching risk settings:", error);
            }
        }
        fetchSettings();
    }, []);

    async function updateSettings() {
        try {
            await fetch("/api/risk-settings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ slippageTolerance, maxGasPrice })
            });
            alert("Risk settings updated successfully!");
        } catch (error) {
            console.error("Error updating risk settings:", error);
        }
    }

    return (
        <Card className="p-4">
            <CardContent>
                <h2 className="text-xl font-bold mb-4">Risk Management Settings</h2>
                <label className="block mb-2">
                    Slippage Tolerance (%):
                    <input
                        type="number"
                        value={slippageTolerance}
                        onChange={(e) => setSlippageTolerance(parseFloat(e.target.value))}
                        className="ml-2 p-1 border rounded"
                    />
                </label>
                <label className="block mb-4">
                    Max Gas Price (Gwei):
                    <input
                        type="number"
                        value={maxGasPrice}
                        onChange={(e) => setMaxGasPrice(parseInt(e.target.value))}
                        className="ml-2 p-1 border rounded"
                    />
                </label>
                <Button onClick={updateSettings}>Update Settings</Button>
            </CardContent>
        </Card>
    );
};

export default RiskSettings;