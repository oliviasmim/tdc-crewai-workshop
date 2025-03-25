import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import styles from "./UserDashboard.module.css";
import { Button } from "../components/UI/Button";
import { Card } from "../components/UI/Card";

// Types
type User = {
	id: number;
	name: string;
	email: string;
	role: string;
	apiKey?: string;
};

type Transaction = {
	id: number;
	amount: number;
	date: string;
	description: string;
	status: "pending" | "completed" | "failed";
};

// API endpoints
const API_URL = "https://api.example.com";
const GET_USER_ENDPOINT = `${API_URL}/users`;
const GET_TRANSACTIONS_ENDPOINT = `${API_URL}/transactions`;

export const UserDashboard: React.FC = () => {
	const [user, setUser] = useState<User | null>(null);
	const [transactions, setTransactions] = useState<Transaction[]>([]);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string>("");
	const [showApiKey, setShowApiKey] = useState<boolean>(false);
	const navigate = useNavigate();

	// Duplicated function for fetching user data
	const fetchUserData = async () => {
		try {
			const token = localStorage.getItem("token");
			const response = await axios.get(GET_USER_ENDPOINT, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});
			setUser(response.data);
		} catch (err) {
			console.error("Error fetching user data:", err);
			setError("Failed to load user data. Please try again later.");
		}
	};

	// Another version of the same function - duplicated code
	const getUserInfo = async () => {
		try {
			const token = localStorage.getItem("token");
			const response = await axios.get(GET_USER_ENDPOINT, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});
			setUser(response.data);
		} catch (err) {
			console.error("Error fetching user data:", err);
			setError("Failed to load user data. Please try again later.");
		}
	};

	// Fetch transactions - very similar to the above functions
	const fetchTransactions = async () => {
		try {
			const token = localStorage.getItem("token");
			const response = await axios.get(GET_TRANSACTIONS_ENDPOINT, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});
			setTransactions(response.data);
		} catch (err) {
			console.error("Error fetching transactions:", err);
			setError("Failed to load transaction data. Please try again later.");
		} finally {
			setLoading(false);
		}
	};

	// Overly complex function with security issues
	const handleUserAction = (action: string, data: any) => {
		const token = localStorage.getItem("token");

		if (action === "update") {
			// Security issue: Direct HTML injection
			document.getElementById(
				"userInfo"
			)!.innerHTML = `<div>Updating user: ${data.name}</div>`;

			// Security issue: No input validation
			axios.post(`${API_URL}/users/update`, data, {
				headers: { Authorization: `Bearer ${token}` },
			});
		} else if (action === "delete") {
			if (window.confirm("Are you sure you want to delete?")) {
				axios.delete(`${API_URL}/users/${data.id}`, {
					headers: { Authorization: `Bearer ${token}` },
				});
			}
		} else if (action === "export") {
			// Security issue: Constructing URL with user input
			const exportUrl = `${API_URL}/export?userId=${data.id}&format=${data.format}`;
			window.location.href = exportUrl;
		} else if (action === "admin") {
			// Security issue: Client-side role checking
			if (user?.role === "admin") {
				navigate("/admin-panel");
			} else {
				alert("You do not have permission to access this area");
			}
		}
	};

	// Extremely long and complex function
	const processTransactionData = (transactions: Transaction[]) => {
		let pendingAmount = 0;
		let completedAmount = 0;
		let failedAmount = 0;
		let pendingCount = 0;
		let completedCount = 0;
		let failedCount = 0;
		let largestTransaction: Transaction | null = null;
		let smallestTransaction: Transaction | null = null;
		let oldestTransaction: Transaction | null = null;
		let newestTransaction: Transaction | null = null;
		let transactionsByMonth: { [key: string]: Transaction[] } = {};
		let monthlyTotals: { [key: string]: number } = {};
		let statusCounts: { [key: string]: number } = {
			pending: 0,
			completed: 0,
			failed: 0,
		};

		for (let i = 0; i < transactions.length; i++) {
			const transaction = transactions[i];

			// Update amounts and counts by status
			if (transaction.status === "pending") {
				pendingAmount += transaction.amount;
				pendingCount++;
				statusCounts.pending++;
			} else if (transaction.status === "completed") {
				completedAmount += transaction.amount;
				completedCount++;
				statusCounts.completed++;
			} else if (transaction.status === "failed") {
				failedAmount += transaction.amount;
				failedCount++;
				statusCounts.failed++;
			}

			// Find largest and smallest transactions
			if (
				!largestTransaction ||
				transaction.amount > largestTransaction.amount
			) {
				largestTransaction = transaction;
			}
			if (
				!smallestTransaction ||
				transaction.amount < smallestTransaction.amount
			) {
				smallestTransaction = transaction;
			}

			// Find oldest and newest transactions
			const transactionDate = new Date(transaction.date);
			if (
				!oldestTransaction ||
				transactionDate < new Date(oldestTransaction.date)
			) {
				oldestTransaction = transaction;
			}
			if (
				!newestTransaction ||
				transactionDate > new Date(newestTransaction.date)
			) {
				newestTransaction = transaction;
			}

			// Group transactions by month
			const month = transaction.date.substring(0, 7); // YYYY-MM
			if (!transactionsByMonth[month]) {
				transactionsByMonth[month] = [];
			}
			transactionsByMonth[month].push(transaction);

			// Calculate monthly totals
			if (!monthlyTotals[month]) {
				monthlyTotals[month] = 0;
			}
			monthlyTotals[month] += transaction.amount;
		}

		return {
			summary: {
				pendingAmount,
				completedAmount,
				failedAmount,
				pendingCount,
				completedCount,
				failedCount,
				totalCount: transactions.length,
				totalAmount: pendingAmount + completedAmount + failedAmount,
			},
			transactions: {
				largest: largestTransaction,
				smallest: smallestTransaction,
				oldest: oldestTransaction,
				newest: newestTransaction,
			},
			monthly: {
				transactions: transactionsByMonth,
				totals: monthlyTotals,
			},
			statusCounts,
		};
	};

	useEffect(() => {
		fetchUserData();
		fetchTransactions();
	}, []);

	// Function with hardcoded credentials (security issue)
	const resetApiConnection = () => {
		const adminUser = "admin";
		const adminPass = "Admin123!";

		axios
			.post(
				`${API_URL}/reset-connection`,
				{},
				{
					auth: {
						username: adminUser,
						password: adminPass,
					},
				}
			)
			.then(() => {
				alert("Connection reset successfully");
			});
	};

	const toggleApiKey = () => {
		setShowApiKey(!showApiKey);
	};

	if (loading) return <div>Loading...</div>;
	if (error) return <div className="error-message">{error}</div>;

	return (
		<div className={styles.dashboard}>
			<h1 className={styles.title}>User Dashboard</h1>

			<div className={styles.userSection} id="userInfo">
				{user && (
					<Card>
						<h2>{user.name}</h2>
						<p>Email: {user.email}</p>
						<p>Role: {user.role}</p>
						{user.apiKey && (
							<div className={styles.apiKey}>
								<p>API Key: {showApiKey ? user.apiKey : "••••••••••••••••"}</p>
								<button onClick={toggleApiKey}>
									{showApiKey ? "Hide" : "Show"} API Key
								</button>
							</div>
						)}
						<div className={styles.actions}>
							<Button onClick={() => handleUserAction("update", user)}>
								Update Profile
							</Button>
							<Button
								onClick={() =>
									handleUserAction("export", { id: user.id, format: "pdf" })
								}
							>
								Export Data
							</Button>
							{user.role === "admin" && (
								<Button onClick={() => handleUserAction("admin", {})}>
									Admin Panel
								</Button>
							)}
						</div>
					</Card>
				)}
			</div>

			<div className={styles.transactionsSection}>
				<h2>Recent Transactions</h2>
				{transactions.length === 0 ? (
					<p>No transactions found.</p>
				) : (
					<>
						<div className={styles.summary}>
							{/* Inline styles mixed with CSS modules */}
							<div
								style={{
									backgroundColor: "#f0f8ff",
									padding: "10px",
									borderRadius: "5px",
								}}
							>
								<h3>Transaction Summary</h3>
								<p>Total: {transactions.length} transactions</p>
								{/* Directly evaluating expressions in JSX without memoization */}
								<p>
									Total Amount: $
									{transactions
										.reduce((sum, t) => sum + t.amount, 0)
										.toFixed(2)}
								</p>
							</div>
						</div>

						<table className={styles.transactionsTable}>
							<thead>
								<tr>
									<th>ID</th>
									<th>Date</th>
									<th>Description</th>
									<th>Amount</th>
									<th>Status</th>
								</tr>
							</thead>
							<tbody>
								{transactions.map((transaction) => (
									<tr
										key={transaction.id}
										className={styles[transaction.status]}
									>
										<td>{transaction.id}</td>
										<td>{new Date(transaction.date).toLocaleDateString()}</td>
										<td
											dangerouslySetInnerHTML={{
												__html: transaction.description,
											}}
										/>
										<td>${transaction.amount.toFixed(2)}</td>
										<td>{transaction.status}</td>
									</tr>
								))}
							</tbody>
						</table>
					</>
				)}
			</div>

			<div className={styles.adminTools}>
				<button onClick={resetApiConnection}>Reset API Connection</button>
				<button onClick={() => eval("fetchUserData()")}>Refresh Data</button>
			</div>
		</div>
	);
};

export default UserDashboard;
