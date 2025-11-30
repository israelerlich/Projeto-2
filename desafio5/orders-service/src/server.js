import express from "express";
import helmet from "helmet";
import ordersRoutes from "./routes/ordersRoutes.js";
import { appConfig } from "./config.js";

const app = express();

app.use(helmet());
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "orders" });
});

app.use(ordersRoutes);

app.listen(appConfig.port, () => {
  console.log(`Orders service listening on port ${appConfig.port}`);
});
