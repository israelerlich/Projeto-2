import { Router } from "express";
import * as userService from "../services/userService.js";

const router = Router();

router.get("/users", (_req, res) => {
  res.json(userService.getAllUsers());
});

router.get("/users/:id", (req, res) => {
  const user = userService.getUserById(req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  res.json(user);
});

export default router;
