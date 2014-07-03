class Blog
  include Cequel::Record

  key :subdomain, :text
  column :name, :text
  column :description, :text
  timestamps

  has_many :posts
end