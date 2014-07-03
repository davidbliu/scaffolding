class PostsController < ActionController::Base
  def show
    Blog.find(current_subdomain).posts.find(params[:id])
  end
end