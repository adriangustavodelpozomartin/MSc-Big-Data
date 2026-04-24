package edu.comillas.restaurants

import edu.comillas.restaurants.model.Restaurant

object RestaurantsUtils {

  /**
   * Devuelve Some(restaurante) si su rating es estrictamente mayor
   * al umbral indicado, o None en caso contrario.
   */
  def filterByRating(r: Restaurant, threshold: Double): Option[Restaurant] = {
    r.rating match {
      case Some(value) if value > threshold => Some(r)
      case _                                 => None
    }
  }

}
