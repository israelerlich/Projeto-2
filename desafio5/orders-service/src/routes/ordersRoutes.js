import { Router } from "express";
import * as orderService from "../services/orderService.js";

const router = Router();

router.get("/orders", (_req, res) => {
  res.json(orderService.getAllOrders());
});

router.get("/orders/:id", (req, res) => {
  const order = orderService.getOrderById(req.params.id);

  if (!order) {
    return res.status(404).json({ message: "Order not found" });
  }

  res.json(order);
});

router.get("/users/:userId/orders", (req, res) => {
  const orders = orderService.getOrdersByUserId(req.params.userId);

  if (!orders.length) {
    return res.status(404).json({ message: "Orders for this user were not found" });
  }

  res.json(orders);
});

export default router;
