class Event
  include Cequel::Record

  key :id, :timeuuid, auto: true
  column :type, :text
  column :title, :text
  column :properties, :text
end