int main(){
    int x, y;

    // pre-conditions
    x = 0;
    y = 1;

    // loop body
    while(unknown()){
        x = x + y;
        if(x <= -100 ){
            y = -y;
        }else if(x >= 100){
            y = -y;
        }else{
            y = y;
        }
    }

    // post-condition
    assert((x >= -100) && (x <= 100));
    
}
