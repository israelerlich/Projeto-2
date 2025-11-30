import { orders } from "../data/orders.js";

export const findAll = () => orders;

export const findById = (id) => orders.find((order) => order.id === id);

export const findByUserId = (userId) => orders.filter((order) => order.userId === userId);
