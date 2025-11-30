import express from "express";
import helmet from "helmet";
import morgan from "morgan";
import axios from "axios";
import { appConfig } from "./config.js";

const app = express();

app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ status: "ok", gateway: true });
});

app.get("/users", async (_req, res) => {
  try {
    const response = await axios.get(`${appConfig.usersServiceUrl}/users`);
    res.json(response.data);
  } catch (error) {
    // Just letting the client know something went wrong downstream.
    res.status(502).json({ message: "Failed to fetch users", detail: error.message });
  }
});

app.get("/users/:id", async (req, res) => {
  try {
    const response = await axios.get(`${appConfig.usersServiceUrl}/users/${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    const statusCode = error.response?.status || 502;
    res.status(statusCode).json({ message: "Failed to fetch user", detail: error.message });
  }
});

app.get("/orders", async (_req, res) => {
  try {
    const response = await axios.get(`${appConfig.ordersServiceUrl}/orders`);
    res.json(response.data);
  } catch (error) {
    res.status(502).json({ message: "Failed to fetch orders", detail: error.message });
  }
});

app.get("/orders/:id", async (req, res) => {
  try {
    const response = await axios.get(`${appConfig.ordersServiceUrl}/orders/${req.params.id}`);
    res.json(response.data);
  } catch (error) {
    const statusCode = error.response?.status || 502;
    res.status(statusCode).json({ message: "Failed to fetch order", detail: error.message });
  }
});

app.listen(appConfig.port, () => {
  console.log(`Gateway running on port ${appConfig.port}`);
});
