#' Equilibrium prevalence of a Ross-Macdonald malaria model.
#'
#' @param a Biting rate (bites per mosquito per day).
#' @param m Ratio of mosquitoes to humans.
#' @param b Probability of transmission, mosquito to human, per bite.
#' @param c Probability of transmission, human to mosquito, per bite.
#' @param r Human recovery rate (per day).
#' @param mu Mosquito mortality rate (per day).
#' @return Equilibrium fraction of humans infected.
#' @examples
#' equilibrium_prevalence(a = 0.3, m = 10, b = 0.5, c = 0.5, r = 0.01, mu = 0.1)
equilibrium_prevalence <- function(a, m, b, c, r, mu) {
  R0 <- (m * a^2 * b * c) / (r * mu)
  if (R0 <= 1) {
    return(0)
  }
  (R0 - 1) / (R0 + (a * c) / mu)
}

#' Fit the model to observed prevalence by least squares over the biting rate.
#'
#' @param data A data frame with a numeric `prevalence` column.
#' @param m,b,c,r,mu Fixed model parameters (see equilibrium_prevalence).
#' @return The fitted biting rate `a`.
fit_prevalence <- function(data, m = 10, b = 0.5, c = 0.5, r = 0.01, mu = 0.1) {
  set.seed(1)
  obj <- function(a) {
    pred <- equilibrium_prevalence(a, m, b, c, r, mu)
    sum((pred - data$prevalence)^2)
  }
  optimise(obj, interval = c(0, 2))$minimum
}
