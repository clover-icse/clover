int main(){
    int x, y;

    // pre-conditions
    x = 50000;
    y = 0;
    

    // loop body
    while(unknown()){
        if(y >= x){
            x = x + 5;
        }else{
            y = y + 1;
        }        
    }

    // post-condition
    if(y > 50000){
        assert((x - y) <= 5);
    }
    
}