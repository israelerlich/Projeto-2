import { users } from "../data/users.js";

export const findAll = () => users;

export const findById = (id) => users.find((user) => user.id === id);
