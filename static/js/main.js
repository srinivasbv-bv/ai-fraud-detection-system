// Main JavaScript Module for AI-Powered Fraud Detection System Dashboard (Indian Payments ₹)

document.addEventListener("DOMContentLoaded", function () {
    console.log("AI Fraud Detection System UI (INR ₹) Initialized.");
    
    if (document.getElementById("decisionChart")) {
        loadDashboardStats();
    }
    if (document.getElementById("prCurveChart")) {
        loadModelMetrics();
    }
    if (document.getElementById("transactionsTableBody")) {
        loadAnalystQueue();
    }
});

// 1. Dashboard Stats Loader
function loadDashboardStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById("kpiTotal").innerText = data.total_transactions;
            document.getElementById("kpiApproved").innerText = data.decisions.approved;
            document.getElementById("kpiStepUp").innerText = data.decisions.step_up;
            document.getElementById("kpiBlocked").innerText = data.decisions.blocked;
            
            renderDecisionChart(data.decisions);
            renderCategoryChart(data.fraud_categories);
        })
        .catch(err => console.error("Error loading dashboard stats:", err));
}

function renderDecisionChart(decisions) {
    const canvas = document.getElementById("decisionChart");
    if (!canvas) return;
    
    if (window.decisionChartInstance) {
        window.decisionChartInstance.destroy();
    }

    const ctx = canvas.getContext("2d");
    window.decisionChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Approve", "Step-Up Auth (OTP/2FA)", "Block"],
            datasets: [{
                data: [decisions.approved, decisions.step_up, decisions.blocked],
                backgroundColor: ["#22c55e", "#f59e0b", "#ef4444"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: "#f8fafc", font: { size: 12 } } }
            }
        }
    });
}

function renderCategoryChart(categories) {
    const canvas = document.getElementById("categoryChart");
    if (!canvas) return;

    if (window.categoryChartInstance) {
        window.categoryChartInstance.destroy();
    }

    const ctx = canvas.getContext("2d");
    const rawLabels = Object.keys(categories);
    const data = Object.values(categories);
    
    // Clean up category label names for display
    const labels = rawLabels.map(l => {
        if (l === 'LEGITIMATE') return 'Legitimate';
        if (l === 'CNP_FRAUD') return 'CNP Fraud';
        if (l === 'ACCOUNT_TAKEOVER') return 'Account Takeover';
        if (l === 'SYNTHETIC_IDENTITY') return 'Synthetic ID';
        if (l === 'VELOCITY_ABUSE') return 'Velocity Abuse';
        if (l === 'CHARGEBACK_FRAUD') return 'Chargeback';
        return l;
    });

    window.categoryChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Transaction Count",
                data: data,
                backgroundColor: "#38bdf8",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: "#cbd5e1" }, grid: { color: "#334155" } },
                y: { ticks: { color: "#cbd5e1" }, grid: { color: "#334155" } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// 2. Interactive Simulator Form Submission
function submitSimulation(event) {
    event.preventDefault();
    
    const payload = {
        amount: parseFloat(document.getElementById("simAmount").value),
        merchant_category: document.getElementById("simMerchant").value,
        device_risk_score: parseFloat(document.getElementById("simDeviceRisk").value),
        location_distance_km: parseFloat(document.getElementById("simLocDist").value),
        account_age_days: parseInt(document.getElementById("simAccAge").value),
        card_age_days: parseInt(document.getElementById("simCardAge").value),
        hour_of_day: parseInt(document.getElementById("simHour").value),
        is_weekend: parseInt(document.getElementById("simWeekend").value),
        velocity_5m: parseInt(document.getElementById("simVelocity").value),
        account_id: document.getElementById("simAccId").value || "ACC_IND_101"
    };

    fetch('/api/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("resultContainer").style.display = "block";
        document.getElementById("riskScoreValue").innerText = result.risk_score;
        
        const decisionBadge = document.getElementById("decisionBadge");
        decisionBadge.innerText = result.decision.replace(/_/g, " ");
        decisionBadge.className = "badge fs-6 p-2 " + (
            result.decision === "APPROVE" ? "badge-approve" :
            result.decision === "STEP_UP_AUTHENTICATION" ? "badge-stepup" : "badge-block"
        );
        
        document.getElementById("recActionText").innerText = result.recommended_action;
        document.getElementById("fraudCatText").innerText = result.framework_mapping.category_name;
        
        document.getElementById("supScoreBar").style.width = result.components.supervised_score + "%";
        document.getElementById("supScoreBar").innerText = result.components.supervised_score + "%";
        
        document.getElementById("seqScoreBar").style.width = result.components.sequence_anomaly_score + "%";
        document.getElementById("seqScoreBar").innerText = result.components.sequence_anomaly_score + "%";
        
        document.getElementById("ruleScoreBar").style.width = result.components.rule_overlay_score + "%";
        document.getElementById("ruleScoreBar").innerText = result.components.rule_overlay_score + "%";
        
        document.getElementById("owaspTag").innerText = result.framework_mapping.owasp_reference;
        document.getElementById("pciTag").innerText = result.framework_mapping.pci_dss_reference;
        document.getElementById("lifecycleTag").innerText = result.framework_mapping.lifecycle_stage;
        
        const rulesList = document.getElementById("triggeredRulesList");
        rulesList.innerHTML = "";
        if (result.triggered_rules.length === 0) {
            rulesList.innerHTML = "<li class='text-muted'>No heuristic rules triggered</li>";
        } else {
            result.triggered_rules.forEach(rule => {
                const li = document.createElement("li");
                li.className = "text-warning";
                li.innerText = rule;
                rulesList.appendChild(li);
            });
        }
    })
    .catch(err => console.error("Error evaluating simulation:", err));
}

// Preset Scenario Loader for Indian Payment System
function loadPresetScenario(scenario) {
    if (scenario === 'LEGITIMATE') {
        document.getElementById("simAmount").value = 250.00;
        document.getElementById("simMerchant").value = "upi_kirana_retail";
        document.getElementById("simDeviceRisk").value = 0.10;
        document.getElementById("simLocDist").value = 3.5;
        document.getElementById("simAccAge").value = 520;
        document.getElementById("simCardAge").value = 300;
        document.getElementById("simHour").value = 14;
        document.getElementById("simVelocity").value = 1;
    } else if (scenario === 'CNP_FRAUD') {
        document.getElementById("simAmount").value = 85000.00;
        document.getElementById("simMerchant").value = "crypto_offshore";
        document.getElementById("simDeviceRisk").value = 0.88;
        document.getElementById("simLocDist").value = 320.0;
        document.getElementById("simAccAge").value = 45;
        document.getElementById("simCardAge").value = 2;
        document.getElementById("simHour").value = 2;
        document.getElementById("simVelocity").value = 2;
    } else if (scenario === 'ATO') {
        document.getElementById("simAmount").value = 250000.00;
        document.getElementById("simMerchant").value = "ecommerce_amazon_flipkart";
        document.getElementById("simDeviceRisk").value = 0.95;
        document.getElementById("simLocDist").value = 2500.0;
        document.getElementById("simAccAge").value = 600;
        document.getElementById("simCardAge").value = 400;
        document.getElementById("simHour").value = 3;
        document.getElementById("simVelocity").value = 4;
    } else if (scenario === 'VELOCITY') {
        document.getElementById("simAmount").value = 8500.00;
        document.getElementById("simMerchant").value = "digital_gaming_rummy";
        document.getElementById("simDeviceRisk").value = 0.75;
        document.getElementById("simLocDist").value = 15.0;
        document.getElementById("simAccAge").value = 180;
        document.getElementById("simCardAge").value = 90;
        document.getElementById("simHour").value = 16;
        document.getElementById("simVelocity").value = 8;
    }
}

// 3. Analyst Queue Loader
function loadAnalystQueue() {
    fetch('/api/transactions')
        .then(res => res.json())
        .then(txns => {
            const tbody = document.getElementById("transactionsTableBody");
            tbody.innerHTML = "";
            
            txns.forEach(t => {
                const tr = document.createElement("tr");
                const badgeClass = t.decision === "APPROVE" ? "badge-approve" :
                                   t.decision === "STEP_UP_AUTHENTICATION" ? "badge-stepup" : "badge-block";
                                   
                tr.innerHTML = `
                    <td><strong>${t.transaction_id}</strong></td>
                    <td>${t.account_id}</td>
                    <td><span class="badge ${badgeClass}">${t.decision.replace(/_/g, " ")}</span></td>
                    <td><strong>${t.risk_score}</strong></td>
                    <td><span class="badge bg-secondary">${t.framework_mapping.category_name}</span></td>
                    <td><small class="text-info">${t.framework_mapping.owasp_reference}</small></td>
                    <td><span class="badge bg-outline-${t.status === 'Pending Review' ? 'warning' : 'success'}">${t.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-success" onclick="updateAction('${t.transaction_id}', 'MARK_LEGITIMATE')">Approve</button>
                        <button class="btn btn-sm btn-outline-danger" onclick="updateAction('${t.transaction_id}', 'CONFIRM_FRAUD')">Block Fraud</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => console.error("Error loading analyst queue:", err));
}

function updateAction(txnId, action) {
    fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transaction_id: txnId, action: action })
    })
    .then(res => res.json())
    .then(data => {
        loadAnalystQueue();
    });
}

// 4. Model Metrics Loader
function loadModelMetrics() {
    fetch('/api/metrics')
        .then(res => res.json())
        .then(data => {
            const primary = data.gradient_boosting || data.random_forest;
            document.getElementById("metricPrecision").innerText = primary.precision;
            document.getElementById("metricRecall").innerText = primary.recall;
            document.getElementById("metricF1").innerText = primary.f1_score;
            document.getElementById("metricAucPr").innerText = primary.auc_pr;
            document.getElementById("metricRocAuc").innerText = primary.roc_auc;
            
            renderMetricsCurves(primary);
        })
        .catch(err => console.error("Error loading model metrics:", err));
}

function renderMetricsCurves(metrics) {
    const canvasPr = document.getElementById("prCurveChart");
    if (canvasPr) {
        if (window.prChartInstance) window.prChartInstance.destroy();
        const ctxPr = canvasPr.getContext("2d");
        window.prChartInstance = new Chart(ctxPr, {
            type: "line",
            data: {
                labels: metrics.pr_curve.recall,
                datasets: [{
                    label: "Precision-Recall Curve",
                    data: metrics.pr_curve.precision,
                    borderColor: "#38bdf8",
                    fill: true,
                    backgroundColor: "rgba(56, 189, 248, 0.15)"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Recall", color: "#cbd5e1" }, ticks: { color: "#cbd5e1" } },
                    y: { title: { display: true, text: "Precision", color: "#cbd5e1" }, ticks: { color: "#cbd5e1" } }
                }
            }
        });
    }

    const canvasRoc = document.getElementById("rocCurveChart");
    if (canvasRoc) {
        if (window.rocChartInstance) window.rocChartInstance.destroy();
        const ctxRoc = canvasRoc.getContext("2d");
        window.rocChartInstance = new Chart(ctxRoc, {
            type: "line",
            data: {
                labels: metrics.roc_curve.fpr,
                datasets: [{
                    label: "ROC Curve (AUC = " + metrics.roc_auc + ")",
                    data: metrics.roc_curve.tpr,
                    borderColor: "#a855f7",
                    fill: true,
                    backgroundColor: "rgba(168, 85, 247, 0.15)"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "False Positive Rate", color: "#cbd5e1" }, ticks: { color: "#cbd5e1" } },
                    y: { title: { display: true, text: "True Positive Rate", color: "#cbd5e1" }, ticks: { color: "#cbd5e1" } }
                }
            }
        });
    }
}
