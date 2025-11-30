import * as userRepository from "../repositories/userRepository.js";

export const getAllUsers = () => userRepository.findAll();

export const getUserById = (id) => userRepository.findById(id);
