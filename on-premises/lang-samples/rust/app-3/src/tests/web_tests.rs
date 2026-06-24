use actix_web::{test, App};

#[actix_rt::test]
async fn test_hello_ok() {
    let app = test::init_service(App::new().service(simple_web::hello)).await;
    let req = test::TestRequest::get().uri("/").to_request();
    let resp = test::call_and_read_body(&app, req).await;
    assert_eq!(resp, "Hello, Rust web!");
}
