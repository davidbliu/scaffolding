class Post
  include Cequel::Record
  belongs_to :blog
  key :id, :timeuuid, auto: true
  column :title, :text
  column :body, :text
end