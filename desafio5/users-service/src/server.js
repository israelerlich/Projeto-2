import express from "express";
import helmet from "helmet";
import usersRoutes from "./routes/usersRoutes.js";
import { appConfig } from "./config.js";

const app = express();

app.use(helmet());
app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({ status: "ok", service: "users" });
});

app.use(usersRoutes);

app.listen(appConfig.port, () => {
  console.log(`Users service listening on port ${appConfig.port}`);
});
