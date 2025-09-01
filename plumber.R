# plumber.R
library(plumber)
library(jsonlite)
library(forecast)

#* Healthcheck
#* @get /health
function(){ list(ok=TRUE) }

#* Simple forecast from numeric series
#* @post /forecast
function(req, res){
  body <- fromJSON(req$postBody)
  series <- as.numeric(body$series)
  horizon <- ifelse(is.null(body$horizon), 12, as.integer(body$horizon))
  ts_data <- ts(series, frequency=12)
  fit <- auto.arima(ts_data)
  f <- forecast::forecast(fit, h=horizon)
  list(
    method=fit$method,
    mean=as.numeric(f$mean),
    lower=as.numeric(f$lower[,2]),
    upper=as.numeric(f$upper[,2])
  )
}
