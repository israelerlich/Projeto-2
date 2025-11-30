import * as orderRepository from "../repositories/orderRepository.js";

export const getAllOrders = () => orderRepository.findAll();

export const getOrderById = (id) => orderRepository.findById(id);

export const getOrdersByUserId = (userId) => orderRepository.findByUserId(userId);
