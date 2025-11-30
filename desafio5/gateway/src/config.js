const port = Number(process.env.PORT || 3000);
const usersServiceUrl = process.env.USERS_SERVICE_URL || "http://localhost:3001";
const ordersServiceUrl = process.env.ORDERS_SERVICE_URL || "http://localhost:3002";

export const appConfig = {
  port,
  usersServiceUrl,
  ordersServiceUrl,
};
