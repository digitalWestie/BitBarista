require 'csv'

#Signature Finder

arr = CSV.read("ready.csv")
arr.delete([])

columns = arr.transpose
columns.delete_at(0) #get rid of times

averages = []
maxmins = []

for column in columns
  averages << column.inject{ |sum, el| sum.to_f + el.to_f }.to_f / column.size
  max = column.inject{ |max, el| max.to_f > el.to_f ? max.to_f : el.to_f }
  min = column.inject{ |min, el| min.to_f < el.to_f ? min.to_f : el.to_f }
  maxmins << [min,max]
end


#max mins
# [[44.28, 67.78], [45.04, 71.96], [11.26, 40.91], [8.53, 39.58], [13.24, 41.06], [47.17, 75.95], [47.72, 81.63], [9.9, 47.58]] 
#averages
# [56.169615384615376, 56.99509615384614, 23.649999999999995, 22.24865384615384, 25.947307692307692, 60.99451923076924, 64.86423076923076, 28.62] 
# average of averages 
# => 42.43617788461538 
